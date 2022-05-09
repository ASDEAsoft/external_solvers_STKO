# ======================================================================================
# ADAPTIVE CYCLIC DISPLACEMENT CONTROL
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

# parameters for adaptive time step
set max_factor __max_factor__
set min_factor __min_factor__
set max_factor_increment __max_factor_incr__
set min_factor_increment __min_factor__
set max_iter __max_iter__
set desired_iter __des_iter__

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
if {$process_id == 0} {
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
	set dU_tolerance [expr abs($dU) * 1.0e-8]
	# compute the monothonic time step for this cycle
	set dT [expr $DT / $nsteps]
	
	if {$process_id == 0} {
		puts "======================================================================"
		puts "CYCLE $i : nsteps = $nsteps; dU = $dU; dT = $dT"
		puts "======================================================================"
	}

	# adaptive time stepping
	set increment_counter 1
	set factor 1.0
	set old_factor $factor
	set dU_cumulative 0.0
	set current_time $itime_old
	while 1 {
		
		if {[expr abs($dU_cumulative - $DU)] <= 1.0e-10} {
			if {$process_id == 0} {
				puts "Target displacement has been reached. Current DU = $dU_cumulative"
				puts "SUCCESS."
			}
			break
		}
		
		set dU_adapt [expr $dU * $factor]
		if {[expr abs($dU_cumulative + $dU_adapt)] > [expr abs($DU) - $dU_tolerance]} {
			set dU_adapt [expr $DU - $dU_cumulative]
		}
		
		set dT_adapt [expr $dT * $dU_adapt/$dU]

		if {$process_id == 0} {
			puts "----------------------------------------------------------------------"
			puts "Increment: $increment_counter. dU_adapt = $dU_adapt. dU_cumulative = $dU_cumulative. dT_adapt = $dT_adapt"
			puts "----------------------------------------------------------------------"
		}
		
		integrator $integrator_type $control_node $control_dof $dU_adapt
		set ok [analyze 1]
		
		if {$ok == 0} {
			set num_iter [testIter]
			
			# print statistics
			set current_time [expr $current_time + $dT_adapt]
			set norms [testNorms]
			if {$num_iter > 0} {set last_norm [lindex $norms [expr $num_iter-1]]} else {set last_norm 0.0}
			if {$process_id == 0} {
				puts "Increment: $increment_counter - Iterations: $num_iter - Norm: $last_norm ( [expr $current_time/$total_duration*100.0] % )"
			}
			
			# Call Custom Functions
			set perc [expr $current_time/$total_duration]
			CustomFunctionCaller $increment_counter $dT $current_time $num_iter $last_norm $perc $process_id $is_parallel
			
			set factor_increment [expr min($max_factor_increment, [expr double($desired_iter) / double($num_iter)])]
			set factor [expr $factor * $factor_increment]
			if {$factor > $max_factor} {
				set factor $max_factor
			}
			if {$factor > $old_factor} {
				if {$process_id == 0} {
					puts "Increasing increment factor due to faster convergence. Factor = $factor"
				}
			}
			set old_factor $factor
			set dU_cumulative [expr $dU_cumulative + $dU_adapt]
			incr increment_counter
			
		} else {
			set num_iter $max_iter
			set factor_increment [expr max($min_factor_increment, [expr double($desired_iter) / double($num_iter)])]
			set factor [expr $factor * $factor_increment]
			if {$process_id == 0} {
				puts "Reducing increment factor due to non convergence. Factor = $factor"
			}
			if {$factor < $min_factor} {
				if {$process_id == 0} {
					puts "ERROR: current factor is less then the minimum allowed ($factor < $min_factor)"
					puts "Giving up"
				}
				error "ERROR: the analysis did not converge"
			}
		}
	}
	# end of adaptive time stepping
}