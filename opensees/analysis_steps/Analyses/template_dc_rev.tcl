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
	set dU_tolerance [expr abs($dU) * 1.0e-8]
	# compute the monothonic time step for this cycle
	set dT [expr $DT / $nsteps]
	set STKO_VAR_initial_time_increment $dT
	
	if {$STKO_VAR_process_id == 0} {
		puts "======================================================================"
		puts "CYCLE $i : nsteps = $nsteps; dU = $dU; dT = $dT"
		puts "======================================================================"
	}

	# adaptive time stepping
	set factor 1.0
	set old_factor $factor
	set dU_cumulative 0.0
	set STKO_VAR_time $itime_old
	while 1 {
		
		# are we done with this cycle?
		if {[expr abs($dU_cumulative - $DU)] <= 1.0e-10} {
			if {$STKO_VAR_process_id == 0} {
				puts "Target displacement has been reached. Current DU = $dU_cumulative"
				puts "SUCCESS."
			}
			break
		}
		
		# adapt the current displacement increment
		set dU_adapt [expr $dU * $factor]
		if {[expr abs($dU_cumulative + $dU_adapt)] > [expr abs($DU) - $dU_tolerance]} {
			set dU_adapt [expr $DU - $dU_cumulative]
		}
		
		# compute the associated monothonic time increment
		set STKO_VAR_time_increment [expr $dT * $dU_adapt/$dU]
		
		# update integrator
		integrator $integrator_type $control_node $control_dof $dU_adapt
		
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
		
		# after analyze
		set STKO_VAR_afterAnalyze_done 0
		STKO_CALL_OnAfterAnalyze
		
		# check convergence
		if {$STKO_VAR_analyze_done == 0} {
			
			# print statistics
			if {$STKO_VAR_process_id == 0} {
				puts [format "Increment: %6d | Iterations: %4d | Norm: %8.3e | Progress: %7.3f %%" $STKO_VAR_increment $STKO_VAR_num_iter  $STKO_VAR_error_norm [expr $STKO_VAR_percentage*100.0]]
			}
			
			# update adaptive factor
			set factor_increment [expr min($max_factor_increment, [expr double($desired_iter) / double($STKO_VAR_num_iter)])]
			
			# check STKO_VAR_afterAnalyze_done. Simulate a reduction similar to non-convergence
			if {$STKO_VAR_afterAnalyze_done != 0} {
				set factor_increment [expr max($min_factor_increment, [expr double($desired_iter) / double($max_iter)])]
				if {$STKO_VAR_process_id == 0} {
					puts "Reducing increment factor due to custom error controls. Factor = $factor"
				}
			}
			
			set factor [expr $factor * $factor_increment]
			if {$factor > $max_factor} {
				set factor $max_factor
			}
			if {$factor > $old_factor} {
				if {$STKO_VAR_process_id == 0} {
					puts "Increasing increment factor due to faster convergence. Factor = $factor"
				}
			}
			set old_factor $factor
			set dU_cumulative [expr $dU_cumulative + $dU_adapt]
			
			# increment time step
			incr STKO_VAR_increment
			
		} else {
			
			# update adaptive factor
			set STKO_VAR_num_iter $max_iter
			set factor_increment [expr max($min_factor_increment, [expr double($desired_iter) / double($STKO_VAR_num_iter)])]
			set factor [expr $factor * $factor_increment]
			if {$STKO_VAR_process_id == 0} {
				puts "Reducing increment factor due to non convergence. Factor = $factor"
			}
			if {$factor < $min_factor} {
				if {$STKO_VAR_process_id == 0} {
					puts "ERROR: current factor is less then the minimum allowed ($factor < $min_factor)"
					puts "Giving up"
				}
				error "ERROR: the analysis did not converge"
			}
		}
		
	}
	# end of adaptive time stepping
}