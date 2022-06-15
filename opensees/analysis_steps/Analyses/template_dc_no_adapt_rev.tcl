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

# choose the correct integrator
if {$STKO_VAR_is_parallel == 1} {
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
set STKO_VAR_increment 1
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
	set STKO_VAR_time_increment [expr $DT / $nsteps]
	
	if {$STKO_VAR_process_id == 0} {
		puts "======================================================================"
		puts "CYCLE $i : nsteps = $nsteps; dU = $dU; dT = $STKO_VAR_time_increment"
		puts "======================================================================"
	}

	set STKO_VAR_time $itime_old
	for {set istep 1} {$istep <= $nsteps} {incr istep; incr STKO_VAR_increment} {
		
		# update integrator
		integrator $integrator_type $control_node $control_dof $dU
		
		# before analyze
		STKO_CALL_OnBeforeAnalyze
		
		# perform this step
		set STKO_VAR_analyze_done [analyze 1]
		
		# update common variables
		if {$STKO_VAR_analyze_done == 0} {
			set STKO_VAR_num_iter [testIter]
			set STKO_VAR_time [expr $STKO_VAR_time + $STKO_VAR_time_increment]
			set STKO_VAR_percentage [expr $STKO_VAR_time/$total_duration]
			set norms [testNorms]
			if {$STKO_VAR_num_iter > 0} {set STKO_VAR_error_norm [lindex $norms [expr $STKO_VAR_num_iter-1]]} else {set STKO_VAR_error_norm 0.0}
		}
		
		# check convergence
		if {$STKO_VAR_analyze_done == 0} {
			# print statistics
			if {$STKO_VAR_process_id == 0} {
				puts [format "Increment: %6d | Iterations: %4d | Norm: %8.3e | Progress: %7.3f %%" $STKO_VAR_increment $STKO_VAR_num_iter  $STKO_VAR_error_norm [expr $STKO_VAR_percentage*100.0]]
			}
		} else {
			# stop analysis
			error "ERROR: the analysis did not converge"
		}
		
		# after analyze
		STKO_CALL_OnAfterAnalyze
	}
	
	# done with this cycle
	if {$STKO_VAR_process_id == 0} {
		puts "Target displacement has been reached. Current U = $iU"
		puts "SUCCESS."
	}
}
