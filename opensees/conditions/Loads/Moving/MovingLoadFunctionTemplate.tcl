if {![info exists STKO_ML_global_mass_dict]} {
	# create the global dictionary if it does not exists yet
	# (only one condition can create it)
	set STKO_ML_global_mass_dict [dict create]
}
# store initial masses before the analysis
for {set path_node_id 0} {$path_node_id < [llength $__path_nodes__]} {incr path_node_id} {
	set inode [lindex $__path_nodes__ $path_node_id]
	set ipid [lindex $__path_partitions__ $path_node_id]
	if {$ipid == [getPID]} {
		# store nodal masses if not yet stored
		if {![dict exists $STKO_ML_global_mass_dict $inode]} {
			set ndf [lindex $__path_nodes_ndf__ $path_node_id]
			set node_masses [lrepeat $ndf 0.0]
			for {set j 1} {$j <= $ndf} {incr j} {lset node_masses [expr $j-1] [expr [nodeMass $inode $j]]}
			dict set STKO_ML_global_mass_dict $inode $node_masses
		}
	}
}
proc __function_before__ {} {
	
	# declare global variables that we may need to access here
	global __pattern__
	global __ts__
	global __path_nodes__
	global __path_nodes_ndf__
	global __path_partitions__
	global __path_positions__
	global __axle_positions__
	global __axle_masses__
	global __axle_forces__
	global __modified_nodes__
	global STKO_ML_global_mass_dict
	global STKO_VAR_increment
	global STKO_VAR_time
	global STKO_VAR_time_increment
	
	# declare local variables
	set T0 __t0__
	set V0 __velocity__
	set P0 __period__
	set num_axles [llength $__axle_positions__]
	set path_num_pts [llength $__path_positions__]
	set path_length [lindex $__path_positions__ [expr $path_num_pts-1]]
	set path_tol [expr $path_length*1.0e-4]
	set this_pid [getPID]
	
	# save nearest nodes data node_info[i] = {node_i {load_i} {mass_i}}
	set node_info [list]
	
	# compute the time of the next analysis call (here we are before the analyze command)
	set T [expr $STKO_VAR_time + $STKO_VAR_time_increment]
	# compute the axle bounds
	set axle_start [lindex $__axle_positions__ 0]
	set axle_end [lindex $__axle_positions__ [expr $num_axles-1]]
	
	# compute the coordinates of the center of the vehicle,
	# taking into account the period
	set Xc_list [list ]
	if {$P0 <= 0.0} {
		set Xc [expr ($T-$T0) * $V0 + $axle_start]
		set Xc_min [expr $Xc + $axle_start]
		set Xc_max [expr $Xc + $axle_end]
		if {$Xc_max >= 0.0 && $Xc_min <= $path_length} {lappend Xc_list $Xc}
	} else {
		# leading center
		set Xc [expr ($T-$T0) * $V0 + $axle_start]
		# max pos leading vehicle
		set Xc_max [expr $Xc + $axle_end]
		# min possible rear axle position
		set Xc_min [expr $axle_start - $axle_end]
		# period to spacing
		set XP0 [expr $P0*$V0]
		set vehicle_count_max [expr max(1, int(($Xc_max - $Xc_min)/$XP0))*2]
		for {set period_counter 0} {$period_counter < $vehicle_count_max} {incr period_counter} {
			set Xc [expr ($T-$T0-$period_counter.0*$P0) * $V0 + $axle_start]
			set Xc_min [expr $Xc + $axle_start]
			set Xc_max [expr $Xc + $axle_end]
			if {$Xc_max >= 0.0 && $Xc_min <= $path_length} { lappend Xc_list $Xc }
		}
	}
	
	# process each Xc
	foreach Xc $Xc_list {
		# process each axle
		for {set axle_id 0} {$axle_id < $num_axles} {incr axle_id} {
			# current axle data
			set iX [lindex $__axle_positions__ $axle_id]
			set iM [lindex $__axle_masses__ $axle_id]
			set iF [lindex $__axle_forces__ $axle_id]
			# compute current position and skip if outside
			set X [expr $Xc + $iX]
			if {$X < 0.0 || $X > $path_length} { continue }
			# find the 2 nodes of the active segment
			set snodes {-1 -1}
			set spos {0 0}
			set spid {0 0}
			set sndf {0 0}
			set sfound 0
			for {set point_id 0} {$point_id < [expr $path_num_pts - 1]} {incr point_id} {
				set point_x [lindex $__path_positions__ [expr $point_id + 1]]
				if {$X <= [expr $point_x + $path_tol]} {
					set snodes [list [lindex $__path_nodes__ $point_id] [lindex $__path_nodes__ [expr $point_id + 1]]]
					set spos [list [lindex $__path_positions__ $point_id] $point_x]
					set spid [list [lindex $__path_partitions__ $point_id] [lindex $__path_partitions__ [expr $point_id + 1]]]
					set sndf [list [lindex $__path_nodes_ndf__ $point_id] [lindex $__path_nodes_ndf__ [expr $point_id + 1]]]
					set sfound 1
					break
				}
			}
			if {$sfound == 0} { error "__function_before__: Cannot find active segment" }
			# compute factors
			set DX [expr [lindex $spos 1] - [lindex $spos 0]]
			set fact_2 [expr ($X - [lindex $spos 0])/$DX]
			set fact_1 [expr 1.0 - $fact_2]
			set sfact [list $fact_1 $fact_2]
			# process each node of the segment if on this partition
			for {set sj 0} {$sj < 2} {incr sj} {
				set sj_pid [lindex $spid $sj]
				if {$sj_pid == $this_pid} {
					set sj_node [lindex $snodes $sj]
					set sj_fact [lindex $sfact $sj]
					set sj_ndf [lindex $sndf $sj]
					# load data Fz
					set sj_Fz [expr $iF * $sj_fact]
					set sj_forces [lrepeat $sj_ndf 0.0]
					lset sj_forces 2 $sj_Fz
					# mass data 
					set sj_masses [lrepeat $sj_ndf 0.0]
					for {set idof 0} {$idof < $sj_ndf} {incr idof} { lset sj_masses $idof [expr [nodeMass $sj_node [expr $idof+1]]] }
					# warning assuming 3D!
					# add axle mass on translational DOFs
					set sj_M [expr $iM * $sj_fact]
					for {set idof 0} {$idof < 3} {incr idof} { lset sj_masses $idof [expr [lindex $sj_masses $idof] + $sj_M] }
					# append info
					lappend node_info [list $sj_node $sj_forces $sj_masses]
				}
			}
		}
	}
	
	# remove previous pattern
	remove loadPattern $__pattern__
	
	# update masses
	set __modified_nodes__ [list]
	foreach info $node_info {
		set node_id [lindex $info 0]
		mass $node_id {*}[lindex $info 2]
		lappend __modified_nodes__ $node_id
	}
	
	# add updated load pattern
	pattern Plain $__pattern__ $__ts__ {
		foreach info $node_info {
			load [lindex $info 0] {*}[lindex $info 1]
		}
	}
}
proc __function_after__ {} {
	global __modified_nodes__
	global STKO_ML_global_mass_dict
	# reset original masses only on nodes modified before this time step
	foreach node_id $__modified_nodes__ {
		set previous_masses [dict get $STKO_ML_global_mass_dict $node_id]
		mass $node_id {*}$previous_masses
	}
}