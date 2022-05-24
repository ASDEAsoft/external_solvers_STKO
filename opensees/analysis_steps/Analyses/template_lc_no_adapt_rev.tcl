# ======================================================================================
# NON-ADAPTIVE LOAD CONTROL ANALYSIS
# ======================================================================================

# ======================================================================================
# USER INPUT DATA 
# ======================================================================================

# duration and initial time step
set total_time __total_time__
set initial_num_incr __initial_num_incr__

set STKO_VAR_time 0.0
set STKO_VAR_time_increment [expr $total_time / $initial_num_incr]
integrator __integrator_type__ $STKO_VAR_time_increment __more_int_data__
for {set STKO_VAR_increment 1} {$STKO_VAR_increment <= $initial_num_incr} {incr STKO_VAR_increment} {
	if {$STKO_VAR_process_id == 0} {
		puts "Increment: $STKO_VAR_increment. time_increment = $STKO_VAR_time_increment. Current time = $STKO_VAR_time"
	}
	
	set ok [analyze 1 ]
	#barrier
	
	if {$ok == 0} {
		set STKO_VAR_num_iter [testIter]
		set STKO_VAR_time [expr $STKO_VAR_time + $STKO_VAR_time_increment]
		set perc [expr $STKO_VAR_time/$total_time]
		# print statistics
		set norms [testNorms]
		if {$STKO_VAR_num_iter > 0} {set STKO_VAR_error_norm [lindex $norms [expr $STKO_VAR_num_iter-1]]} else {set STKO_VAR_error_norm 0.0}
		if {$STKO_VAR_process_id == 0} {
			puts "Increment: $STKO_VAR_increment - Iterations: $STKO_VAR_num_iter - Norm: $STKO_VAR_error_norm ( [expr $perc*100.0] % )"
		}
		
		# Call Custom Functions
		CustomFunctionCaller $perc $STKO_VAR_process_id $STKO_VAR_is_parallel

	} else {
		error "ERROR: the analysis did not converge"
	}
}

if {$STKO_VAR_process_id == 0} {
	puts "Target time has been reached. Current time = $STKO_VAR_time"
	puts "SUCCESS."
}