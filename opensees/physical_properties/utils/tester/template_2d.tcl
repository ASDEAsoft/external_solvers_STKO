model basic -ndm 2 -ndf 2

set time_list [list \
__time__]
set strain_list [list \
__strain__]
timeSeries Path 1 -time $time_list -values $strain_list; #for strain control

timeSeries Linear 2; #for stress control

__materials__

set L __lch__
node 1  0  0
node 2 $L  0
node 3  0 $L
element tri31 1   1 2 3   1.0 __2Dtype__ __tag__

fix 1   1 1
fix 2   0 1

set flags1 [list __flags1__]; #1 = stress controlled, 2 = strain controlled
set flags2 [list __flags2__]; #1 = strain cycle, 2 = strain fixed
set imps   [list __imps__]; # imposed reference stress or strain values

# apply stresses on stress-controlled components
if {[lindex $flags1 0] == 1} { pattern Plain 1 2 -fact [expr $L/2.0] { load 2 [lindex $imps 0] 0 } }; # S11
if {[lindex $flags1 1] == 1} { pattern Plain 2 2 -fact [expr $L/2.0] { load 3 0 [lindex $imps 1] } }; # S22
if {[lindex $flags1 2] == 1} { pattern Plain 3 2 -fact [expr $L/2.0] { load 3 [lindex $imps 2] 0 } }; # S12

# apply strains on strain-controlled components that are fixed (i.e. not using the testing strain cycle)
if {[lindex $flags1 0] == 2} { if {[lindex $flags2 0] == 2} { pattern Plain 10 2 { sp 2 1 [expr $L*[lindex $imps 0]] } } }; # E11
if {[lindex $flags1 1] == 2} { if {[lindex $flags2 1] == 2} { pattern Plain 20 2 { sp 3 2 [expr $L*[lindex $imps 1]] } } }; # E22
if {[lindex $flags1 2] == 2} { if {[lindex $flags2 2] == 2} { pattern Plain 30 2 { sp 3 1 [expr $L*[lindex $imps 2]] } } }; # 2*E12

# first stage, apply stresses incrementally
constraints Transformation
numberer Plain
system UmfPack
test NormDispIncr 1.0e-6 1000 0
algorithm Newton
integrator LoadControl 0.1
analysis Static
set ok [analyze 10]
if {$ok != 0} {
	return
}
loadConst -time 0.0

wipeAnalysis

constraints Transformation
numberer Plain
system UmfPack
test NormDispIncr 1.0e-6 1000 0
algorithm Newton

# apply strain cycle
if {[lindex $flags1 0] == 2} { if {[lindex $flags2 0] == 1} { pattern Plain 100 1 { sp 2 1 $L } } }; # E11
if {[lindex $flags1 1] == 2} { if {[lindex $flags2 1] == 1} { pattern Plain 200 1 { sp 3 2 $L } } }; # E22
if {[lindex $flags1 2] == 2} { if {[lindex $flags2 2] == 1} { pattern Plain 300 1 { sp 3 1 $L } } }; # 2*E12

# second stage, apply strains
set outFile [open "__out__" w+]
set num_step [llength $time_list]
set perc_incr [expr 1.0/$num_step]
set perc 0.0
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
	
	set strain [eleResponse 1 material 1 strain]
	set stress [eleResponse 1 material 1 stress]
	
	puts $outFile "$perc $strain $stress"
	
	# communicate
	puts "__R__$perc|$strain|$stress"
}







