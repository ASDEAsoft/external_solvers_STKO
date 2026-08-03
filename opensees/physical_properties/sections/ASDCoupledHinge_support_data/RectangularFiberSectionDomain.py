import PyMpc.IO

import sys
import numpy as np
from PyMpc import *
from math import sin, cos, pi

import traceback
	
from PySide2.QtCore import (
	QSize,
	Qt,
	QLocale,
	)
from PySide2.QtWidgets import (
	QWidget,
	QDialog,
	QGridLayout,
	QVBoxLayout,
	QHBoxLayout,
	QTabWidget,
	QLabel,
	QPushButton,
	QSizePolicy,
	QSlider,
	QLineEdit,
	QToolButton,
	QComboBox,
	QTableWidget,
	QTableWidgetItem,
	QStyledItemDelegate,
	)

from PySide2.QtGui import (
	QDoubleValidator,
	QKeySequence,
	QGuiApplication,
	QIcon,
	)
import shiboken2
# import random

# import for convex hull
from scipy.spatial import ConvexHull

# Matplotlib utilities
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

params = {	'legend.fontsize': 'x-small',
			'axes.labelsize': 'x-small',
			'axes.titlesize':'x-small',
			'xtick.labelsize':'x-small',
			'ytick.labelsize':'x-small'}

_TOL = 1e-8

_verbose = False

class MyMplCanvas(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
	def __init__(self, parent=None, width=5, height=5, dpi=100, title = '', projection = ''):
		fig = Figure(figsize=(width, height), dpi=dpi)
		FigureCanvas.__init__(self, fig)

		self.control = parent
		self.figure = fig

		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		plt.rcParams.update(params)
		# plt.tick_params(axis='x', which='both')
		# plt.tick_params(axis='y', which='both')

		# Axes for 3D domain
		if projection == '3d':
			self.ax = fig.add_subplot(1,1,1,projection = '3d')
		else:
			self.ax = fig.add_subplot(1,1,1)
		self.ax.set_title(title)
		self.ax.grid()

		self.setParent(parent)

		FigureCanvas.updateGeometry(self)


	# def compute_initial_figure(self):
		# hl_ax_NMy = self.ax_NMy.plot([],[])
		# self.hl_ax_NMy = hl_ax_NMy[0]
		# hl_ax_NMz = self.ax_NMz.plot([],[])
		# self.hl_ax_NMz = hl_ax_NMz[0]
		# hl_ax_NMz = self.ax_NMz.plot([],[])
		# self.hl_ax_NMz = hl_ax_NMz[0]

	# def update_figure(self, x, f, F):
		# # update pdf
		# self.hl_ax_pdf.set_xdata(x)
		# self.hl_ax_pdf.set_ydata(f)
		# # self.hl_ax_pdf.set_xlim(np.min(self.hl_ax_pdf.get_xdata()),np.max(self.hl_ax_pdf.get_xdata()))

		# # update cdf
		# self.hl_ax_cdf.set_xdata(x)
		# self.hl_ax_cdf.set_ydata(F)

		# self.ax_pdf.set_xlim(min(x), max(x))
		# self.ax_pdf.set_ylim(0, max(f)*1.05)
		# self.ax_cdf.set_xlim(min(x), max(x))
		# self.ax_cdf.set_ylim(0, 1)

		# self.draw()
		# # FigureCanvas.updateGeometry(self)

class MaterialsForRectangularSection:
	def __init__(self, fc, eps_c, eps_cu, n, fcc, eps_cc, eps_ccu, nc, Es, fy, eps_su, eps_sy = None, spalling = False):
		# Unconfined concrete
		self.fc = fc if fc < 0 else -fc
		self.eps_c = eps_c if eps_c < 0 else -eps_c
		self.eps_cu = eps_cu if eps_cu < 0 else -eps_cu
		self.n = n
		# Confined concrete
		self.fcc = fcc if fcc < 0 else -fcc
		self.eps_cc = eps_cc if eps_cc < 0 else -eps_cc
		self.eps_ccu = eps_ccu if eps_ccu < 0 else -eps_ccu
		self.nc = nc
		if abs(self.eps_ccu - self.eps_cu) <= _TOL:
			self.spalling = False
		else:
			self.spalling = True
		# Steel
		self.Es = Es
		self.fy = fy
		if Es > 0:
			self.eps_sy = fy/Es
		else:
			self.eps_sy = 0
		self.eps_su = eps_su
		
	def __str__(self):
		return 'Unconfined Concrete: fc = {} eps_c = {} eps_cu = {} n = {}\nConfined Concrete: fcc = {} eps_cc = {} eps_ccu = {} nc = {}\nSteel: Es = {} fy = {} eps_sy = {} eps_su = {}'.format(self.fc,self.eps_c,self.eps_cu,self.n,self.fcc,self.eps_cc,self.eps_ccu,self.nc,self.Es,self.fy,self.eps_sy,self.eps_su)

def print_prop(p):
	if _verbose: print("\tarea:\t\t{};\n\tIyy:\t\t{};\n\tIzz:\t\t{};\n\tJ:\t\t\t{};\n\talphaY:\t\t{};\n\talphaZ:\t\t{};\n\tcentroidY:\t{};\n\tcentroidZ:\t{};\n".format(p.area,p.Iyy,p.Izz,p.J,p.alphaY,p.alphaZ,p.centroidY,p.centroidZ))

class RectangularSectionDomain:
	def __init__(self, w, h, c, sd, yReinf, zReinf, phiReinf, sec, materials):
		self.w = w
		self.h = h
		self.c = c
		self.sd = sd
		self.yReinf = yReinf
		self.zReinf = zReinf
		self.phiReinf = phiReinf
		self.section = sec
		self.materials = materials
		
		# Create the data needed for the computation
		# Create four vertices representing the rectangle of the section
		self.vExt = []
		self.vExt.append(Math.vec3(-self.w/2,-self.h/2,0))
		self.vExt.append(Math.vec3(self.w/2,-self.h/2,0))
		self.vExt.append(Math.vec3(self.w/2,self.h/2,0))
		self.vExt.append(Math.vec3(-self.w/2,self.h/2,0))
		# Create four vertices representing the rectangle of the confined core
		self.vInt = []
		self.wc = self.w - 2 * (self.c+self.sd/2.0)
		self.hc = self.h - 2 * (self.c+self.sd/2.0)
		self.vInt.append(Math.vec3(-self.wc/2,-self.hc/2,0))
		self.vInt.append(Math.vec3(self.wc/2,-self.hc/2,0))
		self.vInt.append(Math.vec3(self.wc/2,self.hc/2,0))
		self.vInt.append(Math.vec3(-self.wc/2,self.hc/2,0))
		# Create four vertices representing the corner steel
		self.vReinf = []
		for y, z in zip(self.yReinf, self.zReinf):
			self.vReinf.append(Math.vec3(y,z,0))
			
		# parameters for computation
		self.nTheta = 32 # number of discretizations in Theta
		self.nAxial = 20 # Number of discretizations in N axis
			
		# Ultimate domain
		# set to None the domain
		self.domain_U = None
		# set to None the deformation profiles
		self.eps_a_U = None
		self.kappa_y_U = None
		self.kappa_z_U = None
		# Yield domain
		# set to None the domain
		self.domain_Y = None
		# set to None the deformation profiles
		self.eps_a_Y = None
		self.kappa_y_Y = None
		self.kappa_z_Y = None
	
	# condition is Y or U for Yield or Ultimate
	def getMyForN(self, N, condition = 'U'): 
		if condition == 'Y':
			if self.domain_Y is None:
				raise Exception("RectangularSectionDomain::getMyForN - Somebody ask to comput My for a given N, but the domain is still None.\nPlease first compute the domain")
			domain = self.domain_Y
		elif condition == 'U':
			if self.domain_U is None:
				raise Exception("RectangularSectionDomain::getMyForN - Somebody ask to comput My for a given N, but the domain is still None.\nPlease first compute the domain")
			domain = self.domain_U
		else:
			raise Exception('RectangularSectionDomain::getMyForN - unknown condition code (should be Y for yield or U for ultimate). Condition asked: {}'.format(condition))

		# find indices of domain with N less and greater than N target
		for i in range(np.size(domain,0)):
			if domain[i,0,0] > N:
				break
		idx1 = i - 1
		idx2 = i 
		N1 = domain[idx1,0,0]
		N2 = domain[idx2,0,0]
		matrix1 = domain[idx1,:,1:]
		matrix2 = domain[idx2,:,1:]
		matrixInterp = (matrix2 - matrix1)/(N2-N1)*(N-N1)+matrix1
		
		My_tmp = np.append(matrixInterp[:,0],matrixInterp[0,0])
		
		return (My_tmp[0],My_tmp[12])
		
	def getkyForN(self, N, condition = 'U'): 
		if condition == 'Y':
			if self.domain_Y is None:
				raise Exception("RectangularSectionDomain::getMyForN - Somebody ask to comput My for a given N, but the domain is still None.\nPlease first compute the domain")
			domain = self.domain_Y
		elif condition == 'U':
			if self.domain_U is None:
				raise Exception("RectangularSectionDomain::getMyForN - Somebody ask to comput My for a given N, but the domain is still None.\nPlease first compute the domain")
			domain = self.domain_U
		else:
			raise Exception('RectangularSectionDomain::getMyForN - unknown condition code (should be Y for yield or U for ultimate). Condition asked: {}'.format(condition))

		# find indices of domain with N less and greater than N target
		for i in range(np.size(domain,0)):
			if domain[i,0,0] > N:
				break
		idx1 = i - 1
		idx2 = i 
		N1 = domain[idx1,0,0]
		N2 = domain[idx2,0,0]
		matrix1 = domain[idx1,:,1:]
		matrix2 = domain[idx2,:,1:]
		matrixInterp = (matrix2 - matrix1)/(N2-N1)*(N-N1)+matrix1
		
		ky_tmp = np.append(matrixInterp[:,2],matrixInterp[0,2])
		
		return (ky_tmp[0],ky_tmp[int(self.nTheta/2)])
		
	def getMzForN(self, N, condition = 'U'):
		if condition == 'Y':
			if self.domain_Y is None:
				raise Exception("RectangularSectionDomain::getMzForN - Somebody ask to comput My for a given N, but the domain is still None.\nPlease first compute the domain")
			domain = self.domain_Y
		elif condition == 'U':
			if self.domain_U is None:
				raise Exception("RectangularSectionDomain::getMzForN - Somebody ask to comput My for a given N, but the domain is still None.\nPlease first compute the domain")
			domain = self.domain_U
		else:
			raise Exception('RectangularSectionDomain::getMzForN - unknown condition code (should be Y for yield or U for ultimate). Condition asked: {}'.format(condition))

		# find indices of domain with N less and greater than N target
		for i in range(np.size(domain,0)):
			if domain[i,0,0] > N:
				break
		idx1 = i - 1
		idx2 = i 
		N1 = domain[idx1,0,0]
		N2 = domain[idx2,0,0]
		matrix1 = domain[idx1,:,1:]
		matrix2 = domain[idx2,:,1:]
		matrixInterp = (matrix2 - matrix1)/(N2-N1)*(N-N1)+matrix1
		
		Mz_tmp = np.append(matrixInterp[:,1],matrixInterp[0,1])
		
		return (Mz_tmp[int(self.nTheta/4)],Mz_tmp[int(3*self.nTheta/4)])
		
	def getkzForN(self, N, condition = 'U'):
		if condition == 'Y':
			if self.domain_Y is None:
				raise Exception("RectangularSectionDomain::getMzForN - Somebody ask to comput My for a given N, but the domain is still None.\nPlease first compute the domain")
			domain = self.domain_Y
		elif condition == 'U':
			if self.domain_U is None:
				raise Exception("RectangularSectionDomain::getMzForN - Somebody ask to comput My for a given N, but the domain is still None.\nPlease first compute the domain")
			domain = self.domain_U
		else:
			raise Exception('RectangularSectionDomain::getMzForN - unknown condition code (should be Y for yield or U for ultimate). Condition asked: {}'.format(condition))

		# find indices of domain with N less and greater than N target
		for i in range(np.size(domain,0)):
			if domain[i,0,0] > N:
				break
		idx1 = i - 1
		idx2 = i 
		N1 = domain[idx1,0,0]
		N2 = domain[idx2,0,0]
		matrix1 = domain[idx1,:,1:]
		matrix2 = domain[idx2,:,1:]
		matrixInterp = (matrix2 - matrix1)/(N2-N1)*(N-N1)+matrix1
		
		kz_tmp = np.append(matrixInterp[:,3],matrixInterp[0,3])
		
		return (kz_tmp[int(self.nTheta/4)],kz_tmp[int(3*self.nTheta/4)])
		
	def computeYieldStrainConditions(self, theta=None, emitterPercentage = None):
		# This function computes the strain profiles that lead to yielding of the section
		# Yield is defined as yield of the first tensile rebar or peak strain of concrete,
		# whichever comes first
		
		#material data needed for the computation
		# STEEL
		# yield deformation for steel
		eps_sy = self.materials.eps_sy
		
		# CONCRETE
		# peak deformation of unconfined concrete
		eps_cp = self.materials.eps_c
		
		# If theta is specified, compute only for that value of theta (This cannot make the computation of the full domain, but just of the desired part). 
		# By default use all thetas to construct the full 3D domain
		if theta is None:
			# angle theta (counter-clockwise rotation)
			thetas = np.linspace(0,2*np.pi,self.nTheta,endpoint=False)
		else:
			thetas = [theta]
			
		# create three lists for eps_a, kappa_y_kappa_z (in the OpenSees ref. system)
		eps_a = []
		kappa_y = []
		kappa_z = []
			
		for th in thetas:
			# For each theta: compute yield strain conditions
			
			# Create a line representing the rotation of the neutral axis
			P0 = Math.vec3(0,0,0)
			P1 = Math.vec3(1,0,0)
			# Vectors representing the rotation of the neutral axis
			vx = Math.vec3(cos(th),sin(th),0)
			vy = Math.vec3(-sin(th),cos(th),0)
			vz = Math.vec3(0,0,1)
			R = Math.mat3(vx,vy,vz)
			q = R.toQuaternion()
			P1 = q.rotate(P1)
			
			# Should not be needed: P1 is already a unit vector and P0 should be 0,0,0 so, uL should be P1
			uL = (P1-P0).normalized()
			# Find the points that definite ultimate strain profile for concrete. Pcls is on compression side, Pcls2 is on tension side
			Pcls = None
			Pcls2 = None
			maxD = 0
			minD = 0
			for v in self.vExt:
				u = v-P0
				d = uL.cross(u)
				# positive distance -> compressed side
				if d.z > maxD:
					maxD = d.z
					Pcls = v
				# negative distance -> tensile side
				if d.z < minD:
					minD = d.z
					Pcls2 = v
			if Pcls is None:
				raise Exception('This should never happen. Contact support')
			# Find the points that definite ultimate strain profile for reinforcement
			Psteel = None
			minD = 0
			for v in self.vReinf:
				u = v-P0
				d = uL.cross(u)
				# negative distance -> tensile side
				if d.z < minD:
					minD = d.z
					Psteel = v
			if Psteel is None:
				raise Exception('This should never happen. Contact support')
				
			# Yield strain conditions for each field:
			# Regions 1-4 pivot on Pcls or Psteel
			# Region 1 - Pivot on Psteel (Yielding on Psteel)
			n = 3
			eps_cls = np.linspace(eps_sy,0,n,endpoint=False)
			eps_steel = np.zeros(n) + eps_sy
			# Region 2 - Pivot on Psteel (up to eps_cp for compressed concrete)
			n = 4
			eps_cls = np.append(eps_cls,np.linspace(0,eps_cp,n, endpoint=False))
			eps_steel = np.append(eps_steel,np.zeros(n)+eps_sy)
			# Region 3 - Pivot on Pcls (from eps_sy to 0 for steel)
			n = 40
			eps_cls = np.append(eps_cls,np.zeros(n)+eps_cp)
			eps_steel = np.append(eps_steel,np.linspace(eps_sy,0,n, endpoint=False))
			# Region 4 - Pivot on Pcls (from 0 to eps_cp for steel)
			n = 6
			eps_cls = np.append(eps_cls,np.zeros(n)+eps_cp)
			eps_steel = np.append(eps_steel,np.linspace(0,eps_cp,n, endpoint=True))
			e3 = 0
			for e1, e2 in zip(eps_cls, eps_steel):
				# Find the plane
				A = -sin(th)
				B = cos(th)
				C = (sin(th)*(Psteel.x-Pcls.x)-cos(th)*(Psteel.y-Pcls.y))/(e2-e1)
				# Compute eps_a to give to opensees
				ea = e2 - (A*(0-Psteel.x)+B*(0-Psteel.y))/C
				kx = -B/C
				ky = -A/C
				eps_a.append(ea)
				kappa_y.append(kx)
				kappa_z.append(ky)
				# Compute strain at fiber Pcls2
				e3 = e2 - (A*(Pcls2.x-Psteel.x)+B*(Pcls2.y-Psteel.y))/C
			# Region 5 - Pivot on Pcls (from e3 to eps_cp for bottom concrete)
			n = 8
			eps_cls = np.zeros(n)+eps_cp
			eps_cls2 = np.linspace(eps_cp,float(e3),n, endpoint=False)
			eps_cls2 = np.flip(eps_cls2,0)
			for e1, e2 in zip(eps_cls, eps_cls2):
				# Find the plane
				A = -sin(th)
				B = cos(th)
				C = (sin(th)*(Pcls2.x-Pcls.x)-cos(th)*(Pcls2.y-Pcls.y))/(e2-e1)
				# Compute eps_a to give to opensees
				ea = e2 - (A*(0-Pcls2.x)+B*(0-Pcls2.y))/C
				kx = -B/C
				ky = -A/C
				eps_a.append(ea)
				kappa_y.append(kx)
				kappa_z.append(ky)

		# Save to the object the strain profiles for yield
		self.eps_a_Y = eps_a
		self.kappa_y_Y = kappa_y
		self.kappa_z_Y = kappa_z
	
	def computeUltimateStrainConditions(self, theta=None, accountSpalling = False, emitterPercentage = None):
		# This function computes the strain profiles that lead to ultimate conditions of the section
		
		#material data needed for the computation
		# STEEL
		# ultimate deformation for steel 
		eps_su = self.materials.eps_su
		# yield deformation for steel
		eps_sy = self.materials.eps_sy
		
		# ultimate deformation of unconfined concrete
		eps_cu = self.materials.eps_cu
		# peak deformation of unconfined concrete
		eps_cp = self.materials.eps_c
		# ultimate deformation of confined concrete
		eps_ccu = self.materials.eps_ccu
		# peak deformation of confined concrete
		eps_ccp = self.materials.eps_cc
		
		# If theta is specified, compute only for that value of theta (This cannot make the computation of the full domain, but just of the desired part). 
		# By default use all thetas to construct the full 3D domain
		if theta is None:
			# angle theta (counter-clockwise rotation)
			thetas = np.linspace(0,2*np.pi,self.nTheta,endpoint=False)
		else:
			thetas = [theta]
		
		# create three lists for eps_a, kappa_y_kappa_z (in the OpenSees ref. system)
		eps_a = []
		kappa_y = []
		kappa_z = []
		# Max N (I need just one for all thetas)
		# TODO (now I have for each theta N min and N max) # Just to improve a bit performance and avoid later computations
		# Min N (I need just 1 for all thetas)
		# TODO (now I have for each theta N min and N max)
		# # I will not emit a sendPercentage because this cycle is super fast
		# totOperations = len(thetas)
		# update_threshold = int(totOperations/10)
		# update_counter = 0
		# i = 0
		# if _verbose: print('Number of thetas: {}'.format(len(thetas)))
		for th in thetas:
			# For each theta: compute ultimate strain conditions
			
			# Create a line representing the rotation of the neutral axis
			P0 = Math.vec3(0,0,0)
			P1 = Math.vec3(1,0,0)
			# Vectors representing the rotation of the neutral axis
			vx = Math.vec3(cos(th),sin(th),0)
			vy = Math.vec3(-sin(th),cos(th),0)
			vz = Math.vec3(0,0,1)
			R = Math.mat3(vx,vy,vz)
			q = R.toQuaternion()
			P1 = q.rotate(P1)
			
			# Should not be needed: P1 is already a unit vector and P0 should be 0,0,0 so, uL should be P1
			uL = (P1-P0).normalized()
			# Find the points that definite ultimate strain profile for concrete. Pcls is on compression side, Pcls2 is on tension side
			Pcls = None
			Pcls2 = None
			maxD = 0
			minD = 0
			if accountSpalling:
				vExt = self.vInt
				eps_cu = eps_ccu
				eps_cp = eps_ccp
			else:
				vExt = self.vExt
			for v in vExt:
				u = v-P0
				d = uL.cross(u)
				# positive distance -> compressed side
				if d.z > maxD:
					maxD = d.z
					Pcls = v
				# negative distance -> tensile side
				if d.z < minD:
					minD = d.z
					Pcls2 = v
			if Pcls is None:
				raise Exception('This should never happen. Contact support')
			# Find the points that definite ultimate strain profile for reinforcement
			Psteel = None
			minD = 0
			for v in self.vReinf:
				u = v-P0
				d = uL.cross(u)
				# negative distance -> tensile side
				if d.z < minD:
					minD = d.z
					Psteel = v
			if Psteel is None:
				raise Exception('This should never happen. Contact support')
			
			# Ultimate strain conditions for each field:
			# Campi 1-4 pivot su Pcls o Psteel
			# Campo 1 - Pivot on Psteel
			n = 3
			eps_cls = np.linspace(eps_su,0,n,endpoint=False)
			# if _verbose: print(eps_cls)
			eps_steel = np.zeros(n) + eps_su
			# Campo 2 - Pivot on Psteel
			n = 4
			eps_cls = np.append(eps_cls,np.linspace(0,eps_cp,n, endpoint=False))
			eps_steel = np.append(eps_steel,np.zeros(n)+eps_su)
			# Campo 2 - Pivot on Psteel
			n = 6
			eps_cls = np.append(eps_cls,np.linspace(eps_cp,eps_cu,n, endpoint=False))
			eps_steel = np.append(eps_steel,np.zeros(n)+eps_su)
			# Campo 3 - Pivot on Pcls
			n = 40
			eps_cls = np.append(eps_cls,np.zeros(n)+eps_cu)
			eps_steel = np.append(eps_steel,np.linspace(eps_su,eps_sy,n, endpoint=False))
			# Campo 4 - Pivot on Pcls
			n = 6
			eps_cls = np.append(eps_cls,np.zeros(n)+eps_cu)
			eps_steel = np.append(eps_steel,np.linspace(eps_sy,0,n, endpoint=True))
			e3 = 0
			for e1, e2 in zip(eps_cls, eps_steel):
				# Find the plane
				A = -sin(th)
				B = cos(th)
				C = (sin(th)*(Psteel.x-Pcls.x)-cos(th)*(Psteel.y-Pcls.y))/(e2-e1)
				# Compute eps_a to give to opensees
				ea = e2 - (A*(0-Psteel.x)+B*(0-Psteel.y))/C
				kx = -B/C
				ky = -A/C
				eps_a.append(ea)
				kappa_y.append(kx)
				kappa_z.append(ky)
				# Compute strain at fiber Pcls2
				e3 = e2 - (A*(Pcls2.x-Psteel.x)+B*(Pcls2.y-Psteel.y))/C

			# Campo 5
			n = 8
			eps_cls = np.zeros(n)+eps_cu
			eps_cls2 = np.linspace(0,float(e3),n, endpoint=False)
			eps_cls2 = np.flip(eps_cls2,0)
			#campo 6
			n = 8
			eps_cls = np.append(eps_cls,np.flip(np.linspace(eps_cp,eps_cu,n, endpoint =False),0))
			eps_cls2 = np.append(eps_cls2, np.flip(np.linspace(eps_cp,0,n,endpoint=False),0))
			for e1, e2 in zip(eps_cls, eps_cls2):
				# Find the plane
				A = -sin(th)
				B = cos(th)
				C = (sin(th)*(Pcls2.x-Pcls.x)-cos(th)*(Pcls2.y-Pcls.y))/(e2-e1)
				# Compute eps_a to give to opensees
				ea = e2 - (A*(0-Pcls2.x)+B*(0-Pcls2.y))/C
				kx = -B/C
				ky = -A/C
				eps_a.append(ea)
				kappa_y.append(kx)
				kappa_z.append(ky)

			# # I don't emit a sendPercentage because this operation is super fast
			# if emitterPercentage is not None:
				# i += 1
				# update_counter += 1
				# # from time import sleep
				# # sleep(0.1)
				# if update_counter >= update_threshold:
					# update_counter = 0
					# if _verbose: print('emit from strain')
					# emitterPercentage(int(i / totOperations * 100))
		
		# Save to the object the strain profiles for ultimate conditions
		self.eps_a_U = eps_a
		self.kappa_y_U = kappa_y
		self.kappa_z_U = kappa_z
		
	def integrate(self,ea, kx, ky):
		N = 0
		Mx = 0
		My = 0
		# debug = False
		# if abs(ea-0.10725190839694657) < 1e-14:
			# if _verbose: print('Debugging: ea = {} - ky = {} - kz = {}'.format(ea,kx,ky))
			# if abs(kx+0.0003816793893129771) < 1e-14:
				# debug = True
		for group in self.section.surfaceFibers:
			for fiber in group.fibers.fibers:
				# compute epsilon for the fiber
				eps = ea - fiber.x * ky + fiber.y * kx
				if fiber.x <= self.wc/2 and fiber.x >= -self.wc/2 and fiber.y >= -self.hc/2 and fiber.y <= self.hc/2:
					# It is confined concrete
					sig = paraboRett(self.materials.fcc,self.materials.eps_cc,self.materials.eps_ccu,self.materials.n,eps)
				else:
					# It is unconfined concrete
					# It is confined concrete
					sig = paraboRett(self.materials.fc,self.materials.eps_c,self.materials.eps_cu,self.materials.n,eps)
				# if debug:
					# if _verbose: print(fiber.x, fiber.y, eps, sig)
				N += sig * fiber.area
				Mx += (sig * fiber.area)* fiber.y
				My += (sig* fiber.area) * (-fiber.x)
		# if debug:
			# if _verbose: print(N, Mx, My)
		for group in self.section.punctualFibers:
			for fiber in group.fibers.fibers:
				# compute epsilon for the fiber
				eps = ea - fiber.x * ky + fiber.y * kx
				sig = elasticPP(self.materials.Es,self.materials.fy,self.materials.eps_su,eps)
				# if debug:
					# if _verbose: print(fiber.x, fiber.y, eps, sig)
				N += sig * fiber.area
				Mx += (sig * fiber.area)* fiber.y
				My += (sig* fiber.area) * (-fiber.x)
		# if debug:
			# if _verbose: print(N, Mx, My)
			# raise Exception("Sono qui")
		return (N, Mx, My)
	
	def computeDomainForCondition(self, emitterPercentage = None, emitterText = None, condition = 'U'):
		
		if condition == 'U':
			# I asked to compute the domain for ultimate conditions
			if self.eps_a_U is None:
				raise Exception("RectangularSectionDomain::computeDomainForCondition - Somebody ask to compute ultimate domain, but strain profiles are empty.\nPlease first compute the ultimate strain profiles")
			eps_a = self.eps_a_U
			kappa_y = self.kappa_y_U
			kappa_z = self.kappa_z_U
			name = 'ultimate'
		elif condition == 'Y':
			# I asked to compute the domain for ultimate conditions
			if self.eps_a_Y is None:
				raise Exception("RectangularSectionDomain::computeDomainForCondition - Somebody ask to compute yield domain, but strain profiles are empty.\nPlease first compute the yield strain profiles")
			eps_a = self.eps_a_Y
			kappa_y = self.kappa_y_Y
			kappa_z = self.kappa_z_Y
			name = 'yield'
		else:
			raise Exception("RectangularSectionDomain::computeDomainForCondition - Unknown code for condition. Should be U (ultimate) or Y (yield). Given {}".format(condition))
			
		if self.section is None:
			raise Exception('Error: Section is None. Cannot compute the domain by integration of strain profiles')
		
		# if _verbose: print("Fiber section properties:")
		# print_prop(self.section.calculateProperties(only_surfaces = True))

		# N, My, Mz in OpenSees reference system
		Nlist = []
		Mylist = []
		Mzlist = []
		kylist = []
		kzlist = []
		
		# numerical integration for obtaining N, Mx, My
		# Compute the number of integrations I need to perform
		totIntegrations = len(self.eps_a_U) 
		update_threshold = int(totIntegrations / 10)
		i = 0
		update_counter = 0
		from time import time
		t0 = time()
		# if _verbose: print('totIntegrations to be done: {}'.format(totIntegrations))
		if emitterText is not None:
			emitterText(f'Integrating {name} strain profiles to compute domain...')
			
		for ea, kx, ky in zip(eps_a, kappa_y, kappa_z):
			N, My, Mz = self.integrate(ea, kx, ky)
			Nlist.append(N)
			Mylist.append(My)
			Mzlist.append(Mz)
			kylist.append(kx)
			kzlist.append(ky)
			if emitterPercentage is not None:
				i += 1
				update_counter += 1
				if update_counter >= update_threshold:
					update_counter = 0
					emitterPercentage(int(i / totIntegrations * 100))
					
		# I have obtained the non-structured domain for forces (PMM) and deformations (Pkk)
		if _verbose: print('RectangularSectionDomain::computeDomainForUltimateConditions -> performed integration in {} s'.format(time() - t0))
		if emitterText is not None:
			emitterText('Integrated profiles. Creating the structured domain...')
		
		t0 = time()
		# Convert them to np arrays
		N = np.array(Nlist)
		My = np.array(Mylist)
		Mz = np.array(Mzlist)
		ky = np.array(kylist)
		kz = np.array(kzlist)
		ea = np.array(eps_a)
		# if _verbose: print('Raw domain - unstructures points')
		# if _verbose: print(' N = np.array({})'.format(N.tolist()))
		# if _verbose: print(' My = np.array({})'.format(My.tolist()))
		# if _verbose: print(' Mz = np.array({})'.format(Mz.tolist()))
		# if _verbose: print(' N = np.array({})'.format(N.tolist()))
		# if _verbose: print(' ky = np.array({})'.format(ky.tolist()))
		# if _verbose: print(' kz = np.array({})'.format(kz.tolist()))
		# if _verbose: print(' ea = np.array({})'.format(ea.tolist()))
		
		# Constraint the data transforming it in the -1 +1 range maybe I don't need it
		Nmax = np.max(N)
		Nmin = np.min(N)
		Mymax = np.max(My)
		Mymin = np.min(My)
		Mzmax = np.max(Mz)
		Mzmin = np.min(Mz)
		kymax = np.max(ky)
		kymin = np.min(ky)
		kzmax = np.max(kz)
		kzmin = np.min(kz)
		
		NMymax = N[np.argmax(My)]
		NMzmax = N[np.argmax(Mz)]
		NMymin = N[np.argmin(My)]
		NMzmin = N[np.argmin(Mz)]
		Nkymax = N[np.argmax(ky)]
		Nkzmax = N[np.argmax(kz)]
		Nkymin = N[np.argmin(ky)]
		Nkzmin = N[np.argmin(kz)]
		
		# create a set of values for N 
		npts_n = self.nAxial
		npts_phi = self.nTheta
		# Discretize the Ns
		Ns = np.linspace(Nmin,Nmax,npts_n)
		# add the specific values of N that correspond to max and min points in M and k
		# points to add:
		addingNs = [NMymax, NMzmax, NMymin, NMzmin, Nkymax, Nkzmax,Nkymin,Nkzmin,0.0]
		addedNs = []
		for Nval in addingNs:
			found = False
			for val in addedNs:
				if abs(val-Nval) < 1e-6:
					found = True
			if not found:
				addedNs.append(Nval)
				Ns = np.append(Ns, Nval)
				npts_n += 1
		
		self.nAxial = npts_n
		
		# Sort the values of N
		Ns.sort()
		# if _verbose: print('Ns = np.array({})'.format(Ns.tolist()))
		
		# Create the domain data structure:
		domain = np.zeros((len(Ns),npts_phi,6)) # N, My, Mz, ky, kz, ea
		lenSingleTheta = int(len(N) / npts_phi)
		if not lenSingleTheta * npts_phi == len(N):
			raise Exception('This should never happen. The number of single theta is not integer. Please contact support')
		# if _verbose: print(lenSingleTheta)
		
		for i,n_val in enumerate(Ns,start=0):
			domain[i,:,0] = n_val
			for j in range(npts_phi):
				search_N = N[j*lenSingleTheta:(j+1)*lenSingleTheta]
				search_My = My[j*lenSingleTheta:(j+1)*lenSingleTheta]
				search_ky = ky[j*lenSingleTheta:(j+1)*lenSingleTheta]
				search_Mz = Mz[j*lenSingleTheta:(j+1)*lenSingleTheta]
				search_kz = kz[j*lenSingleTheta:(j+1)*lenSingleTheta]
				search_ea = ea[j*lenSingleTheta:(j+1)*lenSingleTheta]
				found = False
				for k in range(lenSingleTheta):
					if search_N[k] < n_val:
						found = True
						break
				# if _verbose: print('n_val {} is between {} and {} : {} and {}'.format(n_val,j,j-1,search_N[j],search_N[j-1]))
				# if _verbose: print('ky(j-1) =', search_ky[j-1], 'ky(j) = ', search_ky[j])
				# if _verbose: print('kz(j-1) =', search_kz[j-1], 'kz(j) = ', search_kz[j])
				if (not found) or ((search_N[k-1]-search_N[k]) == 0):
					# if _verbose: print('first if')
					domain[i,j,1] = search_My[k]
					domain[i,j,2] = search_Mz[k]
					domain[i,j,3] = search_ky[k]
					domain[i,j,4] = search_kz[k]
					domain[i,j,5] = search_ea[k]
				else:
					# if _verbose: print('else')
					domain[i,j,1] = search_My[k]+(n_val-search_N[k])*(search_My[k-1]-search_My[k])/(search_N[k-1]-search_N[k])
					domain[i,j,2] = search_Mz[k]+(n_val-search_N[k])*(search_Mz[k-1]-search_Mz[k])/(search_N[k-1]-search_N[k])
					domain[i,j,3] = search_ky[k]+(n_val-search_N[k])*(search_ky[k-1]-search_ky[k])/(search_N[k-1]-search_N[k])
					domain[i,j,4] = search_kz[k]+(n_val-search_N[k])*(search_kz[k-1]-search_kz[k])/(search_N[k-1]-search_N[k])
					domain[i,j,5] = search_ea[k]+(n_val-search_N[k])*(search_ea[k-1]-search_ea[k])/(search_N[k-1]-search_N[k])
		
		# Print The structured domain (to be removed after debug)
		structListN = domain.flatten().tolist()[0::6]
		structListMy = domain.flatten().tolist()[1::6]
		structListMz = domain.flatten().tolist()[2::6]
		structListky = domain.flatten().tolist()[3::6]
		structListkz = domain.flatten().tolist()[4::6]
		structListea = domain.flatten().tolist()[5::6]
		
		if _verbose: print('\nStructured domain in python numpy format: ')
		if _verbose: print('N  = np.array({})'.format(structListN))
		if _verbose: print('My = np.array({})'.format(structListMy))
		if _verbose: print('Mz = np.array({})'.format(structListMz))
		if _verbose: print('ky = np.array({})'.format(structListky))
		if _verbose: print('kz = np.array({})'.format(structListkz))
		if _verbose: print('ea = np.array({})'.format(structListea))
		if _verbose: print('Lengths: ')
		if _verbose: print('N  = {} elements'.format(len(structListN)))
		if _verbose: print('My = {} elements'.format(len(structListMy)))
		if _verbose: print('Mz = {} elements'.format(len(structListMz)))
		if _verbose: print('ky = {} elements'.format(len(structListky)))
		if _verbose: print('kz = {} elements'.format(len(structListkz)))
		if _verbose: print('ea = {} elements'.format(len(structListea)))
		if _verbose: print('\nnN = {} - nTheta = {} - nN * nTheta = {}'.format(npts_n,npts_phi,npts_phi*npts_n))
		# Print it in a tcl format
		if _verbose: 
			print('\nStructured domain in Tcl: ')
			str = 'set listN {'
			n = 1
			for i in range(len(structListN)):
				if (i == (10*n)):
					str += '\\\n'
					n += 1
				if (i!=len(structListN)-1):
					str += '{} '.format(structListN[i])
				else:
					str += '{}'.format(structListN[i])
			str += '}\n'
			str += 'set listMy {'
			n = 1
			for i in range(len(structListMy)):
				if (i == (10*n)):
					str += '\\\n'
					n += 1
				if (i!=len(structListMy)-1):
					str += '{} '.format(structListMy[i])
				else:
					str += '{}'.format(structListMy[i])
			str += '}\n'
			str += 'set listMz {'
			n = 1
			for i in range(len(structListMz)):
				if (i == (10*n)):
					str += '\\\n'
					n += 1
				if (i!=len(structListMz)-1):
					str += '{} '.format(structListMz[i])
				else:
					str += '{}'.format(structListMz[i])
			str += '}\n'
			str += 'set listky {'
			n = 1
			for i in range(len(structListky)):
				if (i == (10*n)):
					str += '\\\n'
					n += 1
				if (i!=len(structListky)-1):
					str += '{} '.format(structListky[i])
				else:
					str += '{}'.format(structListky[i])
			str += '}\n'
			str += 'set listkz {'
			n = 1
			for i in range(len(structListkz)):
				if (i == (10*n)):
					str += '\\\n'
					n += 1
				if (i!=len(structListkz)-1):
					str += '{} '.format(structListkz[i])
				else:
					str += '{}'.format(structListkz[i])
			str += '}\n'
			str += 'set listea {'
			n = 1
			for i in range(len(structListea)):
				if (i == (10*n)):
					str += '\\\n'
					n += 1
				if (i!=len(structListea)-1):
					str += '{} '.format(structListea[i])
				else:
					str += '{}'.format(structListea[i])
			str += '}\n'
			print(str)
		
		#Save the domain in the object
		if condition == 'U':
			# I asked to compute the domain for ultimate conditions
			self.domain_U = domain
		elif condition == 'Y':
			# I asked to compute the domain for yield conditions
			self.domain_Y = domain

def paraboRett(fc,eps_cp,eps_cu,n,eps):
	sig = 0
	if eps < 0.0:
		if eps >= eps_cp:
			# sig = -fc * (1-(1-(eps/eps_cp))**n)
			sig = -fc/(eps_cp**2)*eps**2+2*fc/eps_cp*eps
		elif eps >= eps_cu:
			sig = fc
	return sig
	
def elasticPP(E,fy,eps_su,eps):
	tol = 1e-6
	if abs(eps) - eps_su > tol:
		return 0
	if eps >= 0:
		sign = 1
	else:
		sign = -1
	sig = sign*min(fy,abs(E*eps))
	return sig
	
class ContainerDomainGraphs(QWidget):
	def __init__(self, xlabel, ylabel, zlabel, Nmin, Nmax, parent = None, mainWidgetPtr = None):
		super(ContainerDomainGraphs, self).__init__(parent)
		
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.zlabel = zlabel
		self.Nmin = Nmin
		self.Nmax = Nmax
		
		self.mainWidgetPtr = mainWidgetPtr
		
		# layout
		layout = QGridLayout()
		# matplotlib: 4 graphs for plotting what needed
		# Domain 3D: Top-Left
		self.canvas3d = MyMplCanvas(self, title = 'Domain {}-{}-{}'.format(xlabel,ylabel,zlabel), projection = '3d')
		self.canvas3d.ax.set_xlabel(xlabel)
		self.canvas3d.ax.set_ylabel(ylabel)
		self.canvas3d.ax.set_zlabel(zlabel)
		layout.addWidget(self.canvas3d,1,0,4,4)
		self.navi_toolbar3d = NavigationToolbar(self.canvas3d, self)
		layout.addWidget(self.navi_toolbar3d,5,0,1,4)
		# Top-Right
		self.canvasNMy = MyMplCanvas(self, title = 'Domain {}-{}'.format(xlabel,ylabel))
		self.canvasNMy.ax.set_xlabel(xlabel)
		self.canvasNMy.ax.set_ylabel(ylabel)
		layout.addWidget(self.canvasNMy,1,4,4,4)
		self.navi_toolbarNMy = NavigationToolbar(self.canvasNMy, self)
		layout.addWidget(self.navi_toolbarNMy,5,4,1,4)
		# Bottom-Left
		self.canvasNMz = MyMplCanvas(self, title = 'Domain {}-{}'.format(xlabel,zlabel))
		self.canvasNMz.ax.set_xlabel(xlabel)
		self.canvasNMz.ax.set_ylabel(zlabel)
		layout.addWidget(self.canvasNMz,6,0,4,4)
		self.navi_toolbarNMz = NavigationToolbar(self.canvasNMz, self)
		layout.addWidget(self.navi_toolbarNMz,10,0,1,4)
		# Bottom-Right
		self.canvasMyMz = MyMplCanvas(self, title = 'Domain {}-{}'.format(ylabel,zlabel))
		self.canvasMyMz.ax.set_xlabel(ylabel)
		self.canvasMyMz.ax.set_ylabel(zlabel)
		self.canvasMyMz.ax.set_title('Domain {}-{} (N=0)'.format(ylabel,zlabel))
		
		self.cid = None # By default it is disconnected
		
		layout.addWidget(self.canvasMyMz,6,4,4,4)
		self.navi_toolbarMyMz = NavigationToolbar(self.canvasMyMz, self)
		layout.addWidget(self.navi_toolbarMyMz,10,4,1,4)
		# Create a slider to select N for My-Mz plot
		sliderWidget = QWidget()
		sliderWidget.setLayout(QHBoxLayout())
		sliderWidget.layout().setContentsMargins(0,0,0,0)
		self.sliderN = QSlider()
		self.sliderN.setOrientation(Qt.Orientation.Horizontal)
		self.sliderN.setRange(Nmin,Nmax)
		
		from math import log10
		self.sliderN.setValue(0)
		self.sliderN.setSingleStep(int(10**(max(int(log10(abs(Nmin)))-3,0))))
		self.sliderN.setPageStep(int(10**(max(int(log10(abs(Nmin)))-2,1))))
		self.buttonN0 = QPushButton('N=0')
		self.buttonN0.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		self.buttonN0.setFixedWidth(35)
		self.editN = QLineEdit('0')
		self.editN.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		self.editN.setFixedWidth(65)
		validator = QDoubleValidator(self)
		validator.setBottom(Nmin)
		validator.setTop(Nmax)
		self.editN.setValidator(validator)
		self.buttonDetail = QToolButton()
		self.buttonDetail.setIcon(QIcon(":/odb/fiber_plot"))
		self.buttonDetail.setCheckable(True)
		self.buttonData = QPushButton('Data')
		
		sliderWidget.layout().addWidget(QLabel('N'))
		sliderWidget.layout().addWidget(self.sliderN)
		sliderWidget.layout().addWidget(self.buttonN0)
		sliderWidget.layout().addWidget(self.editN)
		sliderWidget.layout().addWidget(self.buttonDetail)
		sliderWidget.layout().addWidget(self.buttonData)
		
		layout.addWidget(sliderWidget,11,4,1,2)
		
		self.setLayout(layout)
		
		self.domain = None
		
		self.sliderN.valueChanged.connect(self.onSliderValueChanged)
		self.buttonN0.clicked.connect(self.onButtonN0Clicked)
		self.editN.editingFinished.connect(self.onEditingFinishedN)
		self.buttonDetail.toggled.connect(self.onToggledButtonDetail)
		self.buttonData.clicked.connect(self.onButtonDataClicked)
		
	def drawDomain(self,domain,otherDomain = None):
		# Plots
		self.domain = domain
		nThetas = domain.shape[1]
		self.otherDomain = otherDomain # If it is None I will not be able to plot details
		
		# 3d plot
		for i in range(np.size(domain,1)):
			# self.canvas3d.ax.plot(np.append(domain[:,i,0],domain[0,i,0]),np.append(domain[:,i,1],domain[0,i,1]),np.append(domain[:,i,2],domain[0,i,2]),'-r',linewidth=0.5)
			self.canvas3d.ax.plot(domain[:,i,0],domain[:,i,1],domain[:,i,2],'-k',linewidth=0.5)
		for i in range(np.size(domain,0)):
			self.canvas3d.ax.plot(np.append(domain[i,:,0],domain[i,0,0]),np.append(domain[i,:,1],domain[i,0,1]),np.append(domain[i,:,2],domain[i,0,2]),'-ok',linewidth=0.5,markersize=0.5)
		
		# N-My plot
		for i in range(np.size(domain,1)):
			# self.canvasNMy.ax.plot(np.append(domain[:,i,0],domain[0,i,0]),np.append(domain[:,i,1],domain[0,i,1]),'-k',linewidth=0.5,color=(0.8,0.8,0.8))
			self.canvasNMy.ax.plot(domain[:,i,0],domain[:,i,1],'-k',linewidth=0.5,color=(0.8,0.8,0.8))
			# if i == 0:
				# if _verbose: print('x = ', domain[:,i,0])
				# if _verbose: print('y = ',domain[:,i,1])
		self.canvasNMy.ax.plot(domain[:,0,0],domain[:,0,1],'-k')
		self.canvasNMy.ax.plot(domain[:,int(nThetas/2),0],domain[:,int(nThetas/2),1],'-k')
		self.NMy = np.array([np.append(domain[:,0,0],domain[:,int(nThetas/2),0]), np.append(domain[:,0,1],domain[:,int(nThetas/2),1])])
		
		# N-Mz plot
		for i in range(np.size(domain,1)):
			# self.canvasNMz.ax.plot(np.append(domain[:,i,0],domain[0,i,0]),np.append(domain[:,i,2],domain[0,i,2]),'-k',linewidth=0.5,color=(0.8,0.8,0.8))
			self.canvasNMz.ax.plot(domain[:,i,0],domain[:,i,2],'-k',linewidth=0.5,color=(0.8,0.8,0.8))
		self.canvasNMz.ax.plot(domain[:,int(nThetas/4),0],domain[:,int(nThetas/4),2],'-k')
		self.canvasNMz.ax.plot(domain[:,int(nThetas/4*3),0],domain[:,int(nThetas/4*3),2],'-k')
		self.NMz = np.array([np.append(domain[:,int(nThetas/4),0],domain[:,int(nThetas/4*3),0]), np.append(domain[:,int(nThetas/4),2],domain[:,int(nThetas/4*3),2])])
		
		# dominio My-Mz for N fixed
		for i in range(np.size(domain,0)):
			self.canvasMyMz.ax.plot(np.append(domain[i,:,1],domain[i,0,1]),np.append(domain[i,:,2],domain[i,0,2]),'-k',linewidth=0.5,color=(0.8,0.8,0.8))
		# for i in range(np.size(domain,1)):
			# self.canvasMyMz.ax.plot(np.append(domain[:,i,1],domain[0,i,1]),np.append(domain[:,i,2],domain[0,i,2]),'-k',linewidth=0.5,color=(0.9,0.8,0.8))
		# self.canvasMyMz.ax.plot(np.append(matrix1[:,0],matrix1[0,0]),np.append(matrix1[:,1],matrix1[0,1]),'--k',color=(0.7,0.7,0.7))
		# self.canvasMyMz.ax.plot(np.append(matrix2[:,0],matrix2[0,0]),np.append(matrix2[:,1],matrix2[0,1]),'--k',color=(0.7,0.7,0.7))
		
		self.N = 0
		# find indices of domain with N less and greater than N target
		for i in range(np.size(domain,0)):
			# if _verbose: print('N = ',domain[i,0,0])
			if domain[i,0,0] > self.N:
				break
		idx1 = i - 1
		idx2 = i 
		if _verbose: print('indices = ',idx1,idx2)
		N1 = domain[idx1,0,0]
		N2 = domain[idx2,0,0]
		if _verbose: print('Interp between {} and {} with N = {}'.format(N1,N2,self.N))
		matrix1 = domain[idx1,:,1:]
		matrix2 = domain[idx2,:,1:]
		if _verbose: print(matrix1)
		if _verbose: print(matrix2)
		matrixInterp = (matrix2 - matrix1)/(N2-N1)*(self.N-N1)+matrix1
		self.My_tmp = np.append(matrixInterp[:,0],matrixInterp[0,0])
		self.Mz_tmp = np.append(matrixInterp[:,1],matrixInterp[0,1])
		self.MyMz = np.array([self.My_tmp,self.Mz_tmp])
		hMyMz = self.canvasMyMz.ax.plot(self.My_tmp,self.Mz_tmp,'-k') # diego -ok per debug
		self.hMyMz = hMyMz[0]
		
		if self.otherDomain is not None:
			# We interpolate also the other domain.
			# We use it in order to make possible the inspection of the details
			matrix1 = self.otherDomain[idx1,:,:]
			matrix2 = self.otherDomain[idx2,:,:]
			if _verbose: print(matrix1[:,0])
			if _verbose: print(matrix2[:,0])
			if _verbose: print(matrix1[:,1])
			if _verbose: print(matrix2[:,1])
			if _verbose: print(matrix1[:,2])
			if _verbose: print(matrix2[:,2])
			if _verbose: print('r=',(self.N-N1)/(N2-N1))
			matrixInterp = (matrix2 - matrix1)/(N2-N1)*(self.N-N1)+matrix1
			if _verbose: print(matrixInterp)
			self.ky_tmp = np.append(matrixInterp[:,0],matrixInterp[0,0])
			self.kz_tmp = np.append(matrixInterp[:,1],matrixInterp[0,1])
			self.ea_tmp = np.append(matrixInterp[:,2],matrixInterp[0,2])
			if _verbose: print('ky: ',self.ky_tmp)
			if _verbose: print('kz: ',self.kz_tmp)
			if _verbose: print('ea: ',self.ea_tmp)
		
		# #draw also on the 3d domain for the same N
		hMyMz3d = self.canvas3d.ax.plot(np.zeros_like(self.My_tmp),self.My_tmp,self.Mz_tmp,'-b',linewidth = 1.5)
		self.hMyMz3d = hMyMz3d[0]
		
		# draw also on the N-My and N-Mz
		hNMy = self.canvasNMy.ax.plot([0,0],[self.My_tmp[0], self.My_tmp[int(nThetas/2)]],'o--b',markersize=3.0,linewidth=0.75)
		self.hNMy = hNMy[0]
		
		# draw also on the N-My and N-Mz
		hNMz = self.canvasNMz.ax.plot([0,0],[self.Mz_tmp[int(nThetas/4)], self.Mz_tmp[int(nThetas/4*3)]],'o--b',markersize=3.0,linewidth=0.75)
		self.hNMz = hNMz[0]
		
	def onclick(self,event):
		# Manage left click with mouse. If not left click does nothing for now.
		if event.button == 1:
			# First check if any modifier is pressed
			prevent_interp = False
			mods = QGuiApplication.queryKeyboardModifiers()
			if mods == Qt.ShiftModifier:
				# if pressing also shift, prevent interpolation and checks nearest point
				prevent_interp = True
			
			# if _verbose: print('{} click: button={}, x={}, y={}, xdata={}, ydata={}'.format('double' if event.dblclick else 'single', event.button, event.x, event.y, event.xdata, event.ydata))
			
			if _verbose: print('onclick')
			if _verbose: print('Domain My-Mz: ')
			if _verbose: print(self.My_tmp)
			if _verbose: print(self.Mz_tmp)
			if _verbose: print('Other domains:')
			if _verbose: print(self.ky_tmp)
			if _verbose: print(self.kz_tmp)
			if _verbose: print(self.ea_tmp)
			if event.xdata is not None and event.ydata is not None and self.otherDomain is not None:
				# Check the nearest point in the domain My-Mz
				tol = 0.10*max(max(abs(self.My_tmp)),max(abs(self.Mz_tmp)))
				
				def distPoint(P0x,P0y,P1x,P1y):
					return (P1x-P0x)**2 + (P1y-P0y)**2
				
				def distPointLine(P0x,P0y,P1x,P1y,P2x,P2y):
					norm2 = (P2x - P1x) ** 2 + (P2y - P1y) ** 2
					r = (P0x - P1x) * (P2x - P1x) + (P0y - P1y) * (P2y - P1y)
					r /= norm2
					if r < 0:
						return (P1x, P1y, (P1x - P0x) ** 2 + (P1y - P0y) ** 2)
					elif r > 1:
						return (P2x, P2y, (P2x - P0x) ** 2 + (P2y - P0y) ** 2)
					else:
						Px = P1x + r * (P2x-P1x)
						Py = P1y + r * (P2y-P1y)
						return (Px, Py, (Px - P0x) ** 2 + (Py - P0y) ** 2)
						
				dmin = 1e16
				if prevent_interp:
					for i in range(len(self.My_tmp)):
						Px = self.My_tmp[i]
						Py = self.Mz_tmp[i]
						d2 = distPoint(event.xdata, event.ydata, Px, Py)
						if d2 < dmin:
							dmin = d2
							P = [Px, Py]
							idx1 = i
							idx2 = i+1
				else:
					for i in range(len(self.My_tmp)-1):
						Px, Py, d2 = distPointLine(event.xdata, event.ydata, self.My_tmp[i], self.Mz_tmp[i], self.My_tmp[i+1], self.Mz_tmp[i+1])
						if d2 < dmin:
							dmin = d2
							P = [Px, Py]
							idx1 = i
							idx2 = i+1
				if _verbose: print('indices: ',idx1, idx2)
				Px = P[0]
				Py = P[1]
				# if _verbose: print('Found point: ',Px,Py)
				if dmin <= tol**2:
					if _verbose: print('Taken')
					hl_detail = self.canvasMyMz.ax.plot(Px,Py,'or',markersize=4)
					self.canvasMyMz.draw()
				else:
					# if _verbose: print('Discarded')
					# self.canvasMyMz.ax.plot(Px,Py,'oy',markersize=4)
					# self.canvasMyMz.draw()
					Px, Py = None, None
				if Px is not None and Py is not None:
					# Let's try to get the information of everything related to the point
					# Mz = (self.Mz_tmp[idx2]-self.Mz_tmp[idx1])/(self.My_tmp[idx2]-self.My_tmp[idx1])*(Px-self.My_tmp[idx1])+self.Mz_tmp[idx1]
					if _verbose: print('Details for point: N = {} My = {} Mz = {}'.format(self.N,Px,Py))
					# if _verbose: print(Mz)
					# ky = (self.ky_tmp[idx2]-self.ky_tmp[idx1])/(self.My_tmp[idx2]-self.My_tmp[idx1])*(Px-self.My_tmp[idx1])+self.ky_tmp[idx1]
					# kz = (self.kz_tmp[idx2]-self.kz_tmp[idx1])/(self.My_tmp[idx2]-self.My_tmp[idx1])*(Px-self.My_tmp[idx1])+self.kz_tmp[idx1]
					# ea = (self.ea_tmp[idx2]-self.ea_tmp[idx1])/(self.My_tmp[idx2]-self.My_tmp[idx1])*(Px-self.My_tmp[idx1])+self.ea_tmp[idx1]
					# if _verbose: print('My1 = {} - My2 = {} - My = {} ({})'.format(self.My_tmp[idx1],self.My_tmp[idx2],Px,(Px-self.My_tmp[idx1])/(self.My_tmp[idx2]-self.My_tmp[idx1])))
					# if _verbose: print('Mz1 = {} - Mz2 = {} - Mz = {} ({})'.format(self.Mz_tmp[idx1],self.Mz_tmp[idx2],Py,(Py-self.Mz_tmp[idx1])/(self.Mz_tmp[idx2]-self.Mz_tmp[idx1])))
					# if _verbose: print('ky1 = {} - ky2 = {} - ky = {} ({})'.format(self.ky_tmp[idx1],self.ky_tmp[idx2],ky,(ky-self.ky_tmp[idx1])/(self.ky_tmp[idx2]-self.ky_tmp[idx1])))
					# if _verbose: print('kz1 = {} - kz2 = {} - kz = {} ({})'.format(self.kz_tmp[idx1],self.kz_tmp[idx2],kz,(kz-self.kz_tmp[idx1])/(self.kz_tmp[idx2]-self.kz_tmp[idx1])))
					# if _verbose: print('ea1 = {} - ea2 = {} - ea = {} ({})'.format(self.ea_tmp[idx1],self.ea_tmp[idx2],ea,(ea-self.ea_tmp[idx1])/(self.ea_tmp[idx2]-self.ea_tmp[idx1])))
					# if _verbose: print('r Px: ',(Px-self.My_tmp[idx1])/(self.My_tmp[idx2]-self.My_tmp[idx1]))
					# if _verbose: print('r Py: ',(Py-self.Mz_tmp[idx1])/(self.Mz_tmp[idx2]-self.Mz_tmp[idx1]))
					My = Px
					Mz = Py
					r = (My-self.My_tmp[idx1])/(self.My_tmp[idx2]-self.My_tmp[idx1])
					if _verbose: print('r: ',r)
					ky = (self.ky_tmp[idx2]-self.ky_tmp[idx1])*r + self.ky_tmp[idx1]
					kz = (self.kz_tmp[idx2]-self.kz_tmp[idx1])*r + self.kz_tmp[idx1]
					ea = (self.ea_tmp[idx2]-self.ea_tmp[idx1])*r + self.ea_tmp[idx1]
					if _verbose: print('N: {}'.format(self.N))
					if _verbose: print('My: {}'.format(My))
					if _verbose: print('Mz: {}'.format(Mz))
					if _verbose: print('ky: {} ({} - {})'.format(ky,self.ky_tmp[idx1],self.ky_tmp[idx2]))
					if _verbose: print('kz: {} ({} - {})'.format(kz,self.kz_tmp[idx1],self.kz_tmp[idx2]))
					if _verbose: print('ea: {} ({} - {})'.format(ea,self.ea_tmp[idx1],self.ea_tmp[idx2]))
					#Here I open a new widget window with all details for the section in that state
					try:
						# @note Some widgets used here comes from STKO Python API, they are C++ classes exposed to Python via Boost.Python
						# while all other widgets are part of PySide2 and thus exposed via Shiboken2. Since they are incompatible, we use
						# the shiboken2.wrapInstance method on the raw C++ pointer.
						# parentPtr = shiboken2.wrapInstance(self.editor.getPtr(), QWidget)
						if self.ylabel[0] == 'k':
							if _verbose: print('è un dominio in deformazione')
							dialog = DetailSectionResultWidget(self.mainWidgetPtr.getData(), self.N, ky, kz, My, Mz, ea, parent = self)
						else:
							if _verbose: print('è un dominio in forza')
							dialog = DetailSectionResultWidget(self.mainWidgetPtr.getData(), self.N, My, Mz, ky, kz, ea, parent = self)
						# I am not actually using the result
						res = dialog.exec()
						if _verbose: print('Result from dialog Detail: {}'.format(res))
					except:
						exdata = traceback.format_exc().splitlines()
						PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
					# At the end of the process I delete the new Point
					l = hl_detail.pop(0)
					l.remove()
					del l
					self.canvasMyMz.draw()
	
	def onToggledButtonDetail(self, checked):
		if checked:
			self.cid = self.canvasMyMz.mpl_connect('button_press_event', self.onclick)
		else:
			if _verbose: print('The new state is disabled')
			self.canvasMyMz.mpl_disconnect(self.cid)
			
	def onButtonDataClicked(self):
		try:
			dialog = DomainResultDataWidget(NMy = self.NMy, NMz = self.NMz, MyMz = self.MyMz, N = self.N, parent = self)
			res = dialog.exec()
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
	
	def onEditingFinishedN(self):
		self.sliderN.setValue(QLocale().toDouble(self.editN.text())[0])
		
	def onButtonN0Clicked(self):
		self.sliderN.setValue(0)
		# self.onSliderReleased
		
	def onSliderValueChanged(self):
		self.N = self.sliderN.value()
		if self.domain is None:
			return
		
		domain = self.domain
		nThetas = domain.shape[1]
		
		if abs(self.N - self.sliderN.minimum()) < 1e-6:
			self.N = self.sliderN.minimum()*0.999
		if abs(self.N - self.sliderN.maximum()) < 1e-6:
			self.N = self.sliderN.maximum()*0.999
		# find indices of domain with N less and greater than N target
		for i in range(np.size(domain,0)):
			if domain[i,0,0] > self.N:
				break
		idx1 = i - 1
		idx2 = i 
		N1 = domain[idx1,0,0]
		N2 = domain[idx2,0,0]
		matrix1 = domain[idx1,:,1:]
		matrix2 = domain[idx2,:,1:]
		matrixInterp = (matrix2 - matrix1)/(N2-N1)*(self.N-N1)+matrix1
		
		self.My_tmp = np.append(matrixInterp[:,0],matrixInterp[0,0])
		self.Mz_tmp = np.append(matrixInterp[:,1],matrixInterp[0,1])
		self.MyMz = np.array([self.My_tmp,self.Mz_tmp])
		
		# Interp also the other domains!
		if self.otherDomain is not None:
			matrix1 = self.otherDomain[idx1,:,:]
			matrix2 = self.otherDomain[idx2,:,:]
			matrixInterp = (matrix2 - matrix1)/(N2-N1)*(self.N-N1)+matrix1
			self.ky_tmp = np.append(matrixInterp[:,0],matrixInterp[0,0])
			self.kz_tmp = np.append(matrixInterp[:,1],matrixInterp[0,1])
			self.ea_tmp = np.append(matrixInterp[:,2],matrixInterp[0,2])
		
		self.hMyMz.set_xdata(self.My_tmp)
		self.hMyMz.set_ydata(self.Mz_tmp)
		self.canvasMyMz.ax.set_title('Domain {}-{} (N = {:.4e})'.format(self.ylabel,self.zlabel,self.N))
		self.canvasMyMz.draw()
		# # Draw also on the 3d line
		self.hMyMz3d.set_xdata(np.zeros_like(self.My_tmp)+self.N)
		self.hMyMz3d.set_ydata(self.My_tmp)
		self.hMyMz3d.set_3d_properties(self.Mz_tmp)
		self.canvas3d.draw()
		# Draw in the N-My graph
		self.hNMy.set_xdata([self.N, self.N])
		self.hNMy.set_ydata([self.My_tmp[0], self.My_tmp[int(nThetas/2)]])
		self.canvasNMy.draw()
		# Draw in the N-Mz graph
		self.hNMz.set_xdata([self.N, self.N])
		self.hNMz.set_ydata([self.Mz_tmp[int(nThetas/4)], self.Mz_tmp[int(nThetas/4*3)]])
		self.canvasNMz.draw()
		
		self.editN.setText(QLocale().toString(float(self.N)))
		
	
class DomainResultWidget(QDialog):
	def __init__(self, data, parent = None):
		# data is assumed to have the following:
		# A Rectangular section domain for ultimate and yield conditions 
		# TODO: A Rectangular section domain for yield conditions
		# base class initialization
		super(DomainResultWidget, self).__init__(parent)
		
		self.data = data
		
		mainLayout = QVBoxLayout()
		mainLayout.addWidget(QLabel('<html><head/><body><p align="center"><span style=" font-sice:11pt; color:#003399;">Results from domain computation</span></p></body></html>'))
		
		self.tab = QTabWidget()
		mainLayout.addWidget(self.tab)
		
		NminU = np.min(data.domain_U[:,0,0])
		NmaxU = np.max(data.domain_U[:,0,0])
		NminY = np.min(data.domain_Y[:,0,0])
		NmaxY = np.max(data.domain_Y[:,0,0])
		# Create the 4 containers:
		self.containerUltForces = ContainerDomainGraphs('N','My','Mz',NminU,NmaxU,mainWidgetPtr = self)
		self.containerUltForces.drawDomain(data.domain_U[:,:,0:3],data.domain_U[:,:,3:6])
		self.containerUltDefors = ContainerDomainGraphs('N','ky','kz',NminU,NmaxU,mainWidgetPtr = self)
		idxs = np.array([0,3,4])
		self.containerUltDefors.drawDomain(data.domain_U[:,:,idxs],data.domain_U[:,:,np.array([1,2,5])])
		
		self.containerYieldForces = ContainerDomainGraphs('N','My','Mz',NminY,NmaxY,mainWidgetPtr = self)
		self.containerYieldForces.drawDomain(data.domain_Y[:,:,0:3],data.domain_Y[:,:,3:6])
		self.containerYieldDefors = ContainerDomainGraphs('N','ky','kz',NminU,NmaxU,mainWidgetPtr = self)
		idxs = np.array([0,3,4])
		self.containerYieldDefors.drawDomain(data.domain_Y[:,:,idxs],data.domain_Y[:,:,np.array([1,2,5])])
		
		self.tab.addTab(self.containerUltForces,'N-My-Mz Ultimate')
		self.tab.addTab(self.containerUltDefors,'N-ky-kz Ultimate')
		self.tab.addTab(self.containerYieldForces,'N-My-Mz Yield')
		self.tab.addTab(self.containerYieldDefors,'N-ky-kz Yield')

		self.btnClose = QPushButton('Close')
		self.btnClose.setDefault(True)
		self.btnClose.setFocus()
		
		mainLayout.addWidget(self.btnClose)
		
		self.setLayout(mainLayout)
		
		# connections
		self.btnClose.clicked.connect(self.onCloseClicked)
		
	def getData(self):
		return self.data
		

	def onCloseClicked(self):
		self.accept()
		
class DetailSectionResultWidget(QDialog):
	def __init__(self, data, N, My, Mz, ky, kz, ea, parent = None):
		super(DetailSectionResultWidget, self).__init__(parent)
		# Data is an object RectangularDomain
		h = data.h
		w = data.w
		c = data.c
		sd = data.sd
		wc = w - 2 * c - sd
		hc = h - 2 * c - sd
		
		outerX = [-w/2, w/2, w/2, -w/2, -w/2]
		outerY = [-h/2, -h/2, h/2, h/2, -h/2]
		
		innerX = [-wc/2, wc/2, wc/2, -wc/2, -wc/2]
		innerY = [-hc/2, -hc/2, hc/2, hc/2, -hc/2]
		
		yReinf = []
		zReinf = []
		areaReinf = []
		phiReinf = []
		nReinf = 0
		for group in data.section.punctualFibers:
			for fiber in group.fibers.fibers:
				yReinf.append(fiber.x)
				zReinf.append(fiber.y)
				areaReinf.append(fiber.area)
				phiReinf.append((fiber.area * 4 / np.pi)**0.5)
				nReinf += 1
		
		layout = QGridLayout()
		# matplotlib: 2 graphs for plotting what needed
		# Left: strain map
		self.canvasStrain = MyMplCanvas(self, title = 'Strain')
		self.canvasStrain.ax.set_xlabel('y')
		self.canvasStrain.ax.set_ylabel('z')
		layout.addWidget(self.canvasStrain,0,0,4,4)
		self.navi_toolbarStrain = NavigationToolbar(self.canvasStrain, self)
		layout.addWidget(self.navi_toolbarStrain,4,0,1,4)
		# Right: stress map
		self.canvasStress = MyMplCanvas(self, title = 'Stress')
		self.canvasStress.ax.set_xlabel('y')
		self.canvasStrain.ax.set_ylabel('z')
		layout.addWidget(self.canvasStress,0,4,4,4)
		self.navi_toolbarStress = NavigationToolbar(self.canvasStress, self)
		layout.addWidget(self.navi_toolbarStress,4,4,1,4)
		
		# Draw the section
		self.canvasStrain.ax.plot(outerX,outerY,'-k',lw = 1.5)
		self.canvasStrain.ax.plot(innerX,innerY,'-k',lw = 0.75)
		self.canvasStrain.ax.axhline(y=0, c="green", linestyle="-", label="y", lw = 1.0)
		self.canvasStrain.ax.axvline(x=0, c="blue", linestyle="-", label="z", lw = 1.0)

		self.canvasStrain.ax.axis('equal')
		self.canvasStrain.ax.grid(False)
		
		self.canvasStress.ax.plot(outerX,outerY,'-k',lw = 1.5)
		self.canvasStress.ax.plot(innerX,innerY,'-k',lw = 0.75)
		self.canvasStress.ax.axhline(y=0, c="green", linestyle="-", label="y", lw = 1.0)
		self.canvasStress.ax.axvline(x=0, c="blue", linestyle="-", label="z", lw = 1.0)
		self.canvasStress.ax.axis('equal')
		self.canvasStress.ax.grid(False)
		
		# Opzione 1: Plot dei contour
		# Draw the strain and stress contour:
		y = np.linspace(-w/2, w/2, 100)
		z = np.linspace(-h/2, h/2, 100)
		Y, Z = np.meshgrid(y, z)
		E = ea - Y * kz + Z * ky # Here x and y are actually y and z for the se
		S = np.zeros_like(E)
		for i in range(np.size(Y,0)):
			for j in range(np.size(Y,1)):
				if Y[i,j] <= wc/2 and Y[i,j] >= -wc/2 and Z[i,j] >= -hc/2 and Z[i,j] <= hc/2:
					# It is confined concrete
					S[i,j] = paraboRett(data.materials.fcc,data.materials.eps_cc,data.materials.eps_ccu,data.materials.n,E[i,j])
				else:
					# It is unconfined concrete
					S[i,j] = paraboRett(data.materials.fc,data.materials.eps_c,data.materials.eps_cu,data.materials.n,E[i,j])
		vminStrain = E.min()
		vmaxStrain = E.max()
		vminStress = S.min()
		vmaxStress = S.max()
		# cmap = matplotlib.cm.cool
		normStrain = matplotlib.colors.Normalize(vmin=vminStrain, vmax=vmaxStrain)
		normStress = matplotlib.colors.Normalize(vmin=vminStress, vmax=vmaxStress)
		# levels = [eps_cu, eps_cp, 0, eps_sy, 1*(eps_su-eps_sy)/3, 2*(eps_su-eps_sy)/3, eps_su]
		# C1 = self.canvasStress.ax.contourf(Y, Z, E, levels, cmap = 'cool', extend='both');
		C1 = self.canvasStrain.ax.contourf(Y, Z, E, 100, cmap = 'cool', norm = normStrain);
		# Tentativo di label, ma non viene bene.....
		# labelLevels = [C1.levels[0], 0, C1.levels[-1]]
		# print(labelLevels)
		# self.canvasStrain.ax.clabel(C1, fmt='%.5f', colors='w', fontsize=10)
		cbarstrain = self.canvasStrain.figure.colorbar(C1)
		cbarstrain.ax.set_title('\u03B5')
		# cbarstrain.ax.set_title('\u03B5 (\u2030)')
		C2 = self.canvasStress.ax.contourf(Y, Z, S, 100, cmap = 'cool', norm = normStress);
		cbarstress_cls = self.canvasStress.figure.colorbar(C2)
		cbarstress_cls.ax.set_title('\u03c3 c')
		
		from matplotlib.collections import PatchCollection
		from matplotlib.patches import Circle
		
		font = {'family': 'serif',
		'color':  'k',
		'weight': 'normal',
		'size': 8,
		'horizontalalignment': 'center',
		'verticalalignment': 'center',
		}
		
		circles = []
		valuesStrain = []
		valuesStress = []
		for y, z, phi in zip(yReinf,zReinf,phiReinf):
			circles.append(Circle((y,z),phi/2))
			eps = ea - y * kz + z * ky
			sig = elasticPP(data.materials.Es,data.materials.fy,data.materials.eps_su,eps)
			valuesStrain.append(eps)
			valuesStress.append(sig)
			self.canvasStress.ax.text(y,z,'{:.1f}\n'.format(sig),fontdict = font)
			self.canvasStrain.ax.text(y,z,'{:.2f}\u2030\n'.format(eps*1000),fontdict = font)
			
		collection = PatchCollection(circles, cmap = 'cool')
		collection.set_edgecolor('k')
		collection.set_array(np.array(valuesStrain))
		collection.set_clim(vminStrain,vmaxStrain)
		
		self.canvasStrain.ax.add_collection(collection)
		
		collection = PatchCollection(circles, cmap = 'rainbow')
		collection.set_edgecolor('k')
		collection.set_array(np.array(valuesStress))
		# collection.set_clim(vminStress,vmaxStress)
		self.canvasStress.ax.add_collection(collection)
		cbarstress_s = self.canvasStress.figure.colorbar(collection) #,extend='min')
		cbarstress_s.ax.set_title('\u03c3 s')
		
		# # Sarebbe bellissimo, ma non funziona!
		# # def format_coord(x, y):
			# # xarr = Y[0,:]
			# # yarr = Z[:,0]
			# # if ((x > xarr.min()) & (x <= xarr.max()) & 
				# # (y > yarr.min()) & (y <= yarr.max())):
				# # col = np.searchsorted(xarr, x)-1
				# # row = np.searchsorted(yarr, y)-1
				# # z = Z[row, col]
				# # return f'x={x:1.4f}, y={y:1.4f}, z={z:1.4f}   [{row},{col}]'
			# # else:
				# # return f'x={x:1.4f}, y={y:1.4f}'

		# # # # # self.canvasStrain.ax.format_coor = format_coord
		
		# #Alternativa: plottare le fibre direttamente. Di certo più leggero anche se forse più bruttino?
		# ys = []
		# zs = []
		# eps = []
		# sig = []
		# Ncalc = 0
		# Mycalc = 0
		# Mzcalc = 0
		# for group in data.section.surfaceFibers:
			# for fiber in group.fibers.fibers:
				# ys.append(fiber.x)
				# zs.append(fiber.y)
				# # compute epsilon for the fiber
				# eps.append(ea - fiber.x * kz + fiber.y * ky)
				# if fiber.x <= wc/2 and fiber.x >= -wc/2 and fiber.y >= -hc/2 and fiber.y <= hc/2:
					# # It is confined concrete
					# sig.append(paraboRett(data.materials.fcc,data.materials.eps_cc,data.materials.eps_ccu,data.materials.n,ea - fiber.x * kz + fiber.y * ky))
				# else:
					# # It is unconfined concrete
					# sig.append(paraboRett(data.materials.fc,data.materials.eps_c,data.materials.eps_cu,data.materials.n,ea - fiber.x * kz + fiber.y * ky))
				# Ncalc += sig[-1] * fiber.area
				# Mycalc += (sig[-1] * fiber.area)* fiber.y
				# Mzcalc += (sig[-1] * fiber.area) * (-fiber.x)
		# vminStrain = min(eps)
		# vmaxStrain = max(eps)
		# vminStress = min(sig)
		# vmaxStress = max(sig)
		# normStrain = matplotlib.colors.Normalize(vmin=vminStrain, vmax=vmaxStrain)
		# normStress = matplotlib.colors.Normalize(vmin=vminStress, vmax=vmaxStress)
		# scatterStrain = self.canvasStrain.ax.scatter(ys,zs,s=7,c=eps,marker='o',cmap=matplotlib.cm.cool,norm=normStrain)
		# cbarstrain = self.canvasStrain.figure.colorbar(scatterStrain)
		# cbarstrain.ax.set_title('\u03B5')
		# scatterStress = self.canvasStress.ax.scatter(ys,zs,s=7,c=sig,marker='o',cmap=matplotlib.cm.cool,norm=normStress)
		# cbarstress = self.canvasStress.figure.colorbar(scatterStress)
		# cbarstress.ax.set_title('\u03c3 c')
		# font = {'family': 'serif',
		# 'color':  'k',
		# 'weight': 'normal',
		# 'size': 8,
		# 'horizontalalignment': 'center',
		# 'verticalalignment': 'center',
		# }
		# ys = []
		# zs = []
		# eps = []
		# sig = []
		# for group in data.section.punctualFibers:
			# for fiber in group.fibers.fibers:
				# ys.append(fiber.x)
				# zs.append(fiber.y)
				# # compute epsilon for the fiber
				# eps.append(ea - fiber.x * kz + fiber.y * ky)
				# sig.append(elasticPP(data.materials.Es,data.materials.fy,data.materials.eps_su,ea - fiber.x * kz + fiber.y * ky))
				# self.canvasStress.ax.text(fiber.x,fiber.y,'{:.1f}\n'.format(sig[-1]),fontdict = font)
				# Ncalc += sig[-1] * fiber.area
				# Mycalc += (sig[-1] * fiber.area)* fiber.y
				# Mzcalc += (sig[-1] * fiber.area) * (-fiber.x)
		# vminStress = min(sig)
		# vmaxStress = max(sig)
		# normStress = matplotlib.colors.Normalize(vmin=vminStress, vmax=vmaxStress)
		# scatterStrain2 = self.canvasStrain.ax.scatter(ys,zs,s=7,c=eps,marker='o',cmap=matplotlib.cm.cool,norm=normStrain)
		# scatterStress2 = self.canvasStress.ax.scatter(ys,zs,s=7,c=sig,marker='o',cmap=matplotlib.cm.rainbow,norm=normStress)
		# cbarstress2 = self.canvasStress.figure.colorbar(scatterStress2)
		# cbarstress2.ax.set_title('\u03c3 s')
		
		# if _verbose: print('N, My, Mz = {}, {}, {}'.format(N,My,Mz))
		# if _verbose: print('Calculated N, My, Mz = {}, {}, {}'.format(Ncalc,Mycalc,Mzcalc))
		# if _verbose: print('Integrated with the class: ',data.integrate(ea, ky, kz))
		
		# Finalize figures
		self.canvasStrain.ax.xaxis.set_ticks_position('both')
		self.canvasStrain.ax.yaxis.set_ticks_position('both')
		self.canvasStress.ax.xaxis.set_ticks_position('both')
		self.canvasStress.ax.yaxis.set_ticks_position('both')
		
		# set figures left and right to have the same size
		self.canvasStrain.ax.set_position(self.canvasStress.ax.get_position())
		self.canvasStrain.ax.set_xlim(self.canvasStress.ax.get_xlim())
		self.canvasStrain.ax.set_ylim(self.canvasStress.ax.get_ylim())
		
		self.canvasStrain.draw()
		self.canvasStress.draw()
		
		# Close button
		self.btnClose = QPushButton('Close')
		self.btnClose.setDefault(True)
		self.btnClose.setFocus()
		
		layout.addWidget(self.btnClose,5,0,1,8)
		
		self.setLayout(layout)
		
		# connections
		self.btnClose.clicked.connect(self.onCloseClicked)
		
	def onCloseClicked(self):
		self.accept()
		
# custom table widget with copy features
class TableWidget(QTableWidget):
	def __init__(self, parent=None):
		super(TableWidget, self).__init__(parent)

	def keyPressEvent(self, event):
		super(TableWidget, self).keyPressEvent(event)
		try:
			if event.matches(QKeySequence.Copy):
				locale = QLocale()
				ranges = self.selectedRanges()
				if len(ranges) == 1:
					selection = ranges[0]
					data = '\n+'.join(
						'\t+'.join(locale.toString(self.item(i, j).data(Qt.DisplayRole))
								for j in range(selection.leftColumn(), selection.rightColumn() + 1))
						for i in range(selection.topRow(), selection.bottomRow() + 1))
					QGuiApplication.clipboard().setText(data)
		except:
			exdata = traceback.format_exc().splitlines()

class STKODoubleItemDelegate(QStyledItemDelegate):

	def __init__(self, parent=None):
		super(STKODoubleItemDelegate, self).__init__(parent)
		
		# Define Members:
		self.bottom = -sys.float_info.max
		self.top = sys.float_info.max
		self.decimals = 6
		self.edit_decimals = 12
		self.format = 'g'
		self.is_percentage = False
		
	def displayText(self, value, locale):
		a = float(value)
		if self.is_percentage:
			return "{} %".format(locale.toString(a*100.0, self.format, self.decimals))
		else:
			return locale.toString(a, self.format, self.decimals)
	
	def createEditor(self, parent, option, index):
		editor = QLineEdit(parent)
		editor.setValidator(QDoubleValidator(self.bottom, self.top, self.edit_decimals, editor))
		return editor

		
class DomainResultDataWidget(QDialog):
	def __init__(self, NMy, NMz, MyMz, N, parent = None):
		# data is assumed to have the following:
		# A Rectangular section domain for ultimate and yield conditions 
		# TODO: A Rectangular section domain for yield conditions
		# base class initialization
		super(DomainResultDataWidget, self).__init__(parent)
		
		self.NMy = NMy
		self.NMz = NMz
		self.MyMz = MyMz
		self.N = N
		
		mainLayout = QVBoxLayout()
		mainLayout.addWidget(QLabel('<html><head/><body><p align="center"><span style=" font-sice:11pt; color:#003399;">Data from domain computation</span></p></body></html>'))
		
		# Combo box to select data
		self.selectData = QComboBox()
		stringNMy = parent.xlabel + '-' + parent.ylabel
		stringNMz = parent.xlabel + '-' + parent.zlabel
		stringMyMz = parent.ylabel + '-' + parent.zlabel + f' (N={self.N:.3g})'
		self.selectData.addItems([stringNMy, stringNMz, stringMyMz])
		mainLayout.addWidget(self.selectData)
		
		# Table
		self.table = TableWidget()
		self.table.setItemDelegate(STKODoubleItemDelegate(parent = self.table))
		self.table.setColumnCount(2)
		self.updateTable()
		
		mainLayout.addWidget(self.table)
		
		# Close Button
		self.btnClose = QPushButton("Close")
		mainLayout.addWidget(self.btnClose)
		
		self.setLayout(mainLayout)
		
		# connections
		self.btnClose.clicked.connect(self.onCloseClicked)
		self.selectData.currentIndexChanged.connect(self.onSelectDataIndexChanged)
		
	def onCloseClicked(self):
		self.accept()
		
	def onSelectDataIndexChanged(self):
		self.updateTable()
		
	def updateTable(self):
		self.table.setRowCount(0)
		
		if self.selectData.currentIndex() == 0:
			data = self.NMy
			maxIter = self.NMy.size//2
		elif self.selectData.currentIndex() == 1:
			data = self.NMz
			maxIter = self.NMz.size//2
		else:
			data = self.MyMz
			maxIter = self.MyMz.size//2
		
		def make_item(value):
			iy = QTableWidgetItem()
			iy.setData(Qt.DisplayRole, value)
			return iy
		
		for i in range(maxIter):
			self.table.insertRow(i)
			self.table.setItem(i, 0, make_item(data[0,i]))
			self.table.setItem(i, 1, make_item(data[1,i]))
		
		
