# ======================================================================================
# NON-ADAPTIVE CYCLIC DISPLACEMENT CONTROL
# ======================================================================================

# ======================================================================================
# USER INPUT DATA 
# ======================================================================================

# pseudo-time step (monothonic)
set time __time__

# absolute displacement at control node
set U __U__

# control node and dof
set control_node __controlNode__
set control_dof __controlDOF__
set control_node_pid 0; # only for parallel

# initial displacement increment
set trial_disp_incr __trial_disp_incr__

# ======================================================================================
# CALCULATION 
# ======================================================================================

if {$is_parallel == 1} {
	set integrator_type ParallelDisplacementControl
} else {
	set integrator_type DisplacementControl
}

# nuber of cycles
set ncycles [expr [llength $time]-1]
# total duration
set total_duration [lindex $time $ncycles]
if {$STKO_VAR_process_id == 0} {
	puts "TOTAL DURATION: $total_duration"
}

# for each cycle...
for {set i 1} {$i <= $ncycles} {incr i} {
	set itime [lindex $time $i]
	set itime_old [lindex $time [expr $i-1]]
	set iU [lindex $U $i]
	set iU_old [lindex $U [expr $i-1]]
	
	# compute duration and relative displacement for this cycle
	set DT [expr $itime - $itime_old]
	set DU [expr $iU - $iU_old]
	
	# compute required time steps for this cycle
	# in order to achieve the desired trial disp increment
	set nsteps [expr max(1, int(ceil(abs($DU) / abs($trial_disp_incr))))]
	
	# compute the actual displacement increment
	set dU [expr $DU / $nsteps]
	# compute the monothonic time step for this cycle
	set dT [expr $DT / $nsteps]
	
	if {$STKO_VAR_process_id == 0} {
		puts "======================================================================"
		puts "CYCLE $i : nsteps = $nsteps; dU = $dU; dT = $dT"
		puts "======================================================================"
	}

	set current_time $itime_old
	for {set increment_counter 1} {$increment_counter <= $nsteps} {incr increment_counter} {
		
		
		
		integrator $integrator_type $control_node $control_dof $dU
		set ok [analyze 1]
		
		if {$ok == 0} {
			set num_iter [testIter]
			
			# print statistics
			set current_time [expr $current_time + $dT]
			set norms [testNorms]
			if {$num_iter > 0} {set last_norm [lindex $norms [expr $num_iter-1]]} else {set last_norm 0.0}
			if {$STKO_VAR_process_id == 0} {
				puts "Increment: $increment_counter - Iterations: $num_iter - Norm: $last_norm ( [expr $current_time/$total_duration*100.0] % )"
			}
			
			# Call Custom Functions
			set perc [expr $current_time/$total_duration]
			CustomFunctionCaller $increment_counter $dT $current_time $num_iter $last_norm $perc $STKO_VAR_process_id $is_parallel
			
			
		} else {
			error "ERROR: the analysis did not converge"
		}
		
		if {$increment_counter == $nsteps} {
			if {$STKO_VAR_process_id == 0} {
				puts "Target displacement has been reached. Current DU = $dU"
				puts "SUCCESS."
			}
			break
		}
	}
	
	# end of adaptive time stepping
}
