# ======================================================================================
# NON-ADAPTIVE TRANSIENT ANALYSIS
# ======================================================================================

# ======================================================================================
# USER INPUT DATA 
# ======================================================================================

# duration and initial time step
set total_duration __total_time__
set initial_num_incr __initial_num_incr__

set STKO_VAR_time 0.0
set STKO_VAR_time_increment [expr $total_duration / $initial_num_incr]
set STKO_VAR_initial_time_increment $STKO_VAR_time_increment
integrator __integrator_type__ __more_int_data__

for {set STKO_VAR_increment 1} {$STKO_VAR_increment <= $initial_num_incr} {incr STKO_VAR_increment} {
	
	# before analyze
	STKO_CALL_OnBeforeAnalyze
	
	# perform this step
	set STKO_VAR_analyze_done [analyze 1 $STKO_VAR_time_increment]
	
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
			puts "Increment: $STKO_VAR_increment - Iterations: $STKO_VAR_num_iter - Norm: $STKO_VAR_error_norm ( [expr $STKO_VAR_percentage*100.0] % )"
		}
	} else {
		# stop analysis
		error "ERROR: the analysis did not converge"
	}
	
}

# done
if {$STKO_VAR_process_id == 0} {
	puts "Target time has been reached. Current time = $STKO_VAR_time"
	puts "SUCCESS."
}
