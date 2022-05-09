# ======================================================================================
# ADAPTIVE TRANSIENT ANALYSIS
# ======================================================================================

# ======================================================================================
# USER INPUT DATA 
# ======================================================================================

# duration and initial time step
set total_time __total_time__
set initial_num_incr __initial_num_incr__

# parameters for adaptive time step
set max_factor __max_factor__
set min_factor __min_factor__
set max_factor_increment __max_factor_incr__
set min_factor_increment __min_factor__
set max_iter __max_iter__
set desired_iter __des_iter__

set increment_counter 0
set factor 1.0
set old_factor $factor
set time 0.0
set initial_time_increment [expr $total_time / $initial_num_incr]
set time_tolerance [expr abs($initial_time_increment) * 1.0e-8]

while 1 {
	
	incr increment_counter
	if {[expr abs($time)] >= [expr abs($total_time)]} {
		if {$process_id == 0} {
			puts "Target time has been reached. Current time = $time"
			puts "SUCCESS."
		}
		break
	}
	
	set time_increment [expr $initial_time_increment * $factor]
	if {[expr abs($time + $time_increment)] > [expr abs($total_time) - $time_tolerance]} {
		set time_increment [expr $total_time - $time]
	}
	if {$process_id == 0} {
		puts "Increment: $increment_counter. time_increment = $time_increment. Current time = $time"
	}
	
	integrator __integrator_type__ __more_int_data__
	set ok [analyze 1 $time_increment]
	#barrier
	
	if {$ok == 0} {
		set num_iter [testIter]
		set factor_increment [expr min($max_factor_increment, [expr double($desired_iter) / double($num_iter)])]
		set factor [expr $factor * $factor_increment]
		if {$factor > $max_factor} {
			set factor $max_factor
		}
		if {$process_id == 0} {
			if {$factor > $old_factor} {
				puts "Increasing increment factor due to faster convergence. Factor = $factor"
			}
		}
		set old_factor $factor
		set time [expr $time + $time_increment]
		
		# print statistics
		set norms [testNorms]
		if {$num_iter > 0} {set last_norm [lindex $norms [expr $num_iter-1]]} else {set last_norm 0.0}
		if {$process_id == 0} {
			puts "Increment: $increment_counter - Iterations: $num_iter - Norm: $last_norm ( [expr $time/$total_time*100.0] % )"
		}
		
		# Call Custom Functions
		set perc [expr $time/$total_time]
		CustomFunctionCaller $increment_counter $time_increment $time $num_iter $last_norm $perc $process_id $is_parallel
		
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
