model basic -ndm 1 -ndf 1

set time_list [list \
__time__]
set strain_list [list \
__strain__]
timeSeries Path 1 -time $time_list -values $strain_list

__materials__

set L __lch__
node 1 0
node 2 $L
element truss 1 1 2 1.0 __tag__

fix 1 1

pattern Plain 1 1 {
	sp 2 1 $L
}

set outFile [open "__out__" w+]

set num_step [llength $time_list]
set perc_incr [expr 1.0/$num_step]
set perc 0.0

constraints Transformation
numberer Plain
system UmfPack
test NormDispIncr 1.0e-6 1000 0
algorithm Newton

set lambda_old 0.0
for {set i 0} {$i < $num_step} {incr i} {
	
	set perc [expr $perc + $perc_incr]
	
	set lambda [lindex $time_list $i]
	set d_lambda [expr $lambda - $lambda_old]
	set lambda_old $lambda
	
	integrator LoadControl $d_lambda
	analysis Static
	set ok [analyze 1]
	if {$ok != 0} {
		break
	}
	
	reactions
	set strain [lindex $strain_list $i]
	set stress [expr [nodeReaction 2 1]]
	
	puts $outFile [format "%.5E %.5E %.5E" $perc $strain $stress]
	
	# communicate
	puts "__R__$perc $strain $stress"
}

close $outFile





