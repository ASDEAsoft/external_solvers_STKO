model basic -ndm 1 -ndf 1

reliability

__definitions__

set outFile [open "__out__" w+]

set x_start [getInverseCDF __tag__ 0.001]
set x_end [getInverseCDF __tag__ 0.999]
set x_list {}
set num __num__
for {set i 0} {$i < $num} {incr i} {
	lappend x_list [expr ($x_end - $x_start)/$num*$i+$x_start]
}

set num_step [llength $x_list]
set perc_incr [expr 1.0/$num_step]
set perc 0.0

for {set i 0} {$i < $num_step} {incr i} {

	set perc [expr $perc + $perc_incr]

	set x [lindex $x_list $i]

	set f [getPDF __tag__ $x]

	set F [getCDF __tag__ $x]

	puts $outFile [format "%.5E %.5E %.5E %.5E" $perc $x $f $F]

	# communicate
	puts "__R__$perc $x $f $F"
}
