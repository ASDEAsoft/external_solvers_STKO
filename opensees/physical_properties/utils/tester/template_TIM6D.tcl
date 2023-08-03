model basic -ndm 3 -ndf 6

set time_list [list \
__time__]
set deformation_list [list \
__strain__]
timeSeries Path 1 -time $time_list -values $deformation_list; #for deformation control

timeSeries Linear 2; #for stress control

__materials__

node 1  0  0  0; # soil
node 2  0  0  0; # stru
# @Note: compression is positive!
element zeroLengthND 1 1 2  __tag__  -orient -1.0 0.0 0.0 0.0 1.0 0.0

fix 1   1 1 1  1 1 1
fix 2   __freedofs__

set flags1 [list __flags1__]; #1 = force controlled, 2 = deformation controlled
set flags2 [list __flags2__]; #1 = deformation cycle, 2 = deformation fixed
set imps   [list __imps__]; # imposed reference force or deformation values

# apply forces on force-controlled components
if {[lindex $flags1 0] == 1} { pattern Plain 1 2  { load 2 [lindex $imps 0] 0 0   0 0 0 } }; # Q1
if {[lindex $flags1 1] == 1} { pattern Plain 2 2  { load 2 0 [lindex $imps 1] 0   0 0 0 } }; # Q2
if {[lindex $flags1 2] == 1} { pattern Plain 3 2  { load 2 0 0 [lindex $imps 2]   0 0 0 } }; # Q3
if {[lindex $flags1 3] == 1} { pattern Plain 4 2  { load 2 0 0 0   [lindex $imps 3] 0 0 } }; # QR1
if {[lindex $flags1 4] == 1} { pattern Plain 5 2  { load 2 0 0 0   0 [lindex $imps 4] 0 } }; # QR2
if {[lindex $flags1 5] == 1} { pattern Plain 6 2  { load 2 0 0 0   0 0 [lindex $imps 5] } }; # QR3

# apply deformation on deformation-controlled components that are fixed (i.e. not using the testing deformation cycle)
if {[lindex $flags1 0] == 2} { if {[lindex $flags2 0] == 2} { pattern Plain 10 2 { sp 2 1 [lindex $imps 0] } } }; # q1
if {[lindex $flags1 1] == 2} { if {[lindex $flags2 1] == 2} { pattern Plain 20 2 { sp 2 2 [lindex $imps 1] } } }; # q2
if {[lindex $flags1 2] == 2} { if {[lindex $flags2 2] == 2} { pattern Plain 30 2 { sp 2 3 [lindex $imps 2] } } }; # q3
if {[lindex $flags1 3] == 2} { if {[lindex $flags2 3] == 2} { pattern Plain 40 2 { sp 2 4 [lindex $imps 3] } } }; # qr1
if {[lindex $flags1 4] == 2} { if {[lindex $flags2 4] == 2} { pattern Plain 50 2 { sp 2 5 [lindex $imps 4] } } }; # qr2
if {[lindex $flags1 5] == 2} { if {[lindex $flags2 5] == 2} { pattern Plain 60 2 { sp 2 6 [lindex $imps 5] } } }; # qr3

# first stage, apply forces incrementally
constraints Transformation
numberer Plain
system UmfPack
test NormDispIncr 1.0e-8 1000 0
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
test NormDispIncr 1.0e-8 1000 0
algorithm Newton

# apply deformation cycle
if {[lindex $flags1 0] == 2} { if {[lindex $flags2 0] == 1} { pattern Plain 100 1 { sp 2 1 1.0 } } }; # q1
if {[lindex $flags1 1] == 2} { if {[lindex $flags2 1] == 1} { pattern Plain 200 1 { sp 2 2 1.0 } } }; # q2
if {[lindex $flags1 2] == 2} { if {[lindex $flags2 2] == 1} { pattern Plain 300 1 { sp 2 3 1.0 } } }; # q3
if {[lindex $flags1 3] == 2} { if {[lindex $flags2 3] == 1} { pattern Plain 400 1 { sp 2 4 1.0 } } }; # qr1
if {[lindex $flags1 4] == 2} { if {[lindex $flags2 4] == 1} { pattern Plain 500 1 { sp 2 5 1.0 } } }; # qr2
if {[lindex $flags1 5] == 2} { if {[lindex $flags2 5] == 1} { pattern Plain 600 1 { sp 2 6 1.0 } } }; # qr3

# second stage, apply deformation
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
	
	set deformation [eleResponse 1 deformation]
	set force [eleResponse 1 force]
	
	# communicate
	puts "__R__$perc|$deformation|$force"
}







