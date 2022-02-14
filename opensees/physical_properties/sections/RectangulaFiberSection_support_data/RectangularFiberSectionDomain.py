import PyMpc.IO
import matplotlib
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PyMpc import *
from math import sin, cos

pi = 3.14159265359

class MaterialsForRectangularSection:
	def __init__(self, fc, eps_c, eps_cu, n, fcc, eps_cc, eps_ccu, nc, Es, fy, eps_su):
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
		# Steel
		self.Es = Es
		self.fy = fy
		if Es > 0:
			self.eps_sy = fy/Es
		else:
			self.eps_sy = 0
		self.eps_su = eps_su
		
	def __str__(self):
		return 'Unconfined Concrete: fc = {} eps_c = {} eps_cu = {} n = {}\nConfined Concrete: fcc = {} eps_cc = {} eps_ccu = {} nc = {}\nSteel: fy = {} Es = {} eps_sy = {} eps_su = {}'.format(self.fc,self.eps_c,self.eps_cu,self.n,self.fcc,self.eps_cc,self.eps_ccu,self.nc,self.fy,self.Es,self.eps_sy,self.eps_su)
		

def print_prop(p):
	print("\tarea:\t\t{};\n\tIyy:\t\t{};\n\tIzz:\t\t{};\n\tJ:\t\t\t{};\n\talphaY:\t\t{};\n\talphaZ:\t\t{};\n\tcentroidY:\t{};\n\tcentroidZ:\t{};\n".format(p.area,p.Iyy,p.Izz,p.J,p.alphaY,p.alphaZ,p.centroidY,p.centroidZ))

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
	
	def computeUltimateStrainConditions(self, theta=None, accountSpalling = False):
	
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
		
		if self.section is None:
			raise Exception('Error: Section is None. Cannot compute the domain')
		
		print("Fiber section properties:")
		print_prop(self.section.calculateProperties(only_surfaces = True))
		
		# Create the data needed for the computation
		# Create four vertices representing the rectangle of the section
		vExt = []
		vExt.append(Math.vec3(-self.w/2,-self.h/2,0))
		vExt.append(Math.vec3(self.w/2,-self.h/2,0))
		vExt.append(Math.vec3(self.w/2,self.h/2,0))
		vExt.append(Math.vec3(-self.w/2,self.h/2,0))
		# Create four vertices representing the rectangle of the confined core
		vInt = []
		wc = self.w - 2 * (self.c+self.sd/2.0)
		hc = self.h - 2 * (self.c+self.sd/2.0)
		vInt.append(Math.vec3(-wc/2,-hc/2,0))
		vInt.append(Math.vec3(wc/2,-hc/2,0))
		vInt.append(Math.vec3(wc/2,hc/2,0))
		vInt.append(Math.vec3(-wc/2,hc/2,0))
		# Create four vertices representing the corner steel
		vReinf = []
		for y, z in zip(self.yReinf, self.zReinf):
			vReinf.append(Math.vec3(y,z,0))
		
		if theta is None:
			# angle theta (counter-clockwise rotation)
			thetas = np.linspace(0,2*np.pi,32,endpoint=False)
		else:
			thetas = [theta]
		
		# create three lists for eps_a, kappa_y_kappa_z (in the OpenSees ref. system)
		eps_a = []
		kappa_y = []
		kappa_z = []
		# Max N (I need just one for all thetas)
		# Min N (I need just 1 for all thetas)
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
			for v in vReinf:
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
			# print(eps_cls)
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
				# # Just for debug, to erase later
				# plt.figure()
				# # plt.gca().add_patch(patches.Rectangle((vExt[0].x,vExt[0].y),w,h,linewidth=1,edgecolor='k',facecolor=None))
				# # plt.gca().add_patch(patches.Rectangle((vInt[0].x,vInt[0].y),wc,hc,linewidth=1,edgecolor='k',facecolor=None))
				# plt.plot([vExt[0].x, vExt[1].x, vExt[2].x, vExt[3].x, vExt[0].x],[vExt[0].y, vExt[1].y, vExt[2].y, vExt[3].y, vExt[0].y],'-k',linewidth=0.75)
				# plt.plot([vInt[0].x, vInt[1].x, vInt[2].x, vInt[3].x, vInt[0].x],[vInt[0].y, vInt[1].y, vInt[2].y, vInt[3].y, vInt[0].y],'-k',linewidth=0.75)
				# # plot contour of the plane
				# x = np.linspace(-w/1.5, w/1.5, 100)
				# y = np.linspace(-h/1.5, h/1.5, 100)
				# X, Y = np.meshgrid(x, y)
				# Z = e2 - (A*(X-Psteel.x)+B*(Y-Psteel.y))/C
				# levels = np.append(np.linspace(eps_cu,0,8),np.linspace(eps_sy,eps_su,12))
				# # levels = [eps_cu, eps_cp, 0, eps_sy, 1*(eps_su-eps_sy)/3, 2*(eps_su-eps_sy)/3, eps_su]
				# C1 = plt.contourf(X, Y, Z, levels, cmap = 'cool', extend='both');
				# C1.cmap.set_under((0,0,1,0.5))
				# C1.cmap.set_over((1,0,0,0.5))
				# C2 = plt.contour(X,Y,Z,[eps_cu,0,eps_su],colors=('b','g','r'),linewidths=(3,))
				# plt.text(0,0,'eps_a = {:.4f} %'.format(ea*100))
				# plt.text(w/6,-h/6,'k_x = {:.6f} %'.format(kx*100))
				# plt.text(-5*w/6,h/4,'k_y = {:.6f} %'.format(ky*100))
				# # #Draw the inclined line with direction of NA
				# # t = np.linspace(0,1,3)
				# # x = P0.x + t*(P1.x*200-P0.x)
				# # y = P0.y + t*(P1.y*200-P0.y)
				# # plt.plot(x,y,'-k')
				# plt.plot([vReinf[0].x, vReinf[1].x, vReinf[2].x, vReinf[3].x],[vReinf[0].y, vReinf[1].y, vReinf[2].y, vReinf[3].y],'ok')
				# plt.plot(Pcls.x,Pcls.y,'ob',markerSize = 3)
				# plt.plot(Psteel.x,Psteel.y,'or', markerSize = 3)
				# plt.gca().axis('equal')
				# cbar = plt.colorbar(C1);
				# cbar.add_lines(C2)
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
				# # Just for debug, to erase later
				# plt.figure()
				# # plt.gca().add_patch(patches.Rectangle((vExt[0].x,vExt[0].y),w,h,linewidth=1,edgecolor='k',facecolor=None))
				# # plt.gca().add_patch(patches.Rectangle((vInt[0].x,vInt[0].y),wc,hc,linewidth=1,edgecolor='k',facecolor=None))
				# plt.plot([vExt[0].x, vExt[1].x, vExt[2].x, vExt[3].x, vExt[0].x],[vExt[0].y, vExt[1].y, vExt[2].y, vExt[3].y, vExt[0].y],'-k',linewidth=0.75)
				# plt.plot([vInt[0].x, vInt[1].x, vInt[2].x, vInt[3].x, vInt[0].x],[vInt[0].y, vInt[1].y, vInt[2].y, vInt[3].y, vInt[0].y],'-k',linewidth=0.75)
				# # plot contour of the plane
				# x = np.linspace(-w/1.5, w/1.5, 500)
				# y = np.linspace(-h/1.5, h/1.5, 500)
				# X, Y = np.meshgrid(x, y)
				# Z = e2 - (A*(X-Psteel.x)+B*(Y-Psteel.y))/C
				# levels = np.append(np.linspace(eps_cu,0,8),np.linspace(eps_sy,eps_su,12))
				# # levels = [eps_cu, eps_cp, 0, eps_sy, 1*(eps_su-eps_sy)/3, 2*(eps_su-eps_sy)/3, eps_su]
				# C1 = plt.contourf(X, Y, Z, levels, cmap = 'cool', extend='both');
				# C1.cmap.set_under((0,0,1,0.5))
				# C1.cmap.set_over((1,0,0,0.5))
				# C2 = plt.contour(X,Y,Z,[eps_cu,0,eps_su],colors=('b','g','r'),linewidths=(3,))
				# plt.text(0,0,'eps_a = {:.4f} %'.format(ea*100))
				# plt.text(w/6,-h/6,'k_x = {:.6f} %'.format(kx*100))
				# plt.text(-5*w/6,h/4,'k_y = {:.6f} %'.format(ky*100))
				# # #Draw the inclined line with direction of NA
				# # t = np.linspace(0,1,3)
				# # x = P0.x + t*(P1.x*200-P0.x)
				# # y = P0.y + t*(P1.y*200-P0.y)
				# # plt.plot(x,y,'-k')
				# plt.plot([vReinf[0].x, vReinf[1].x, vReinf[2].x, vReinf[3].x],[vReinf[0].y, vReinf[1].y, vReinf[2].y, vReinf[3].y],'ok')
				# plt.plot(Pcls.x,Pcls.y,'ob',markerSize = 3)
				# plt.plot(Psteel.x,Psteel.y,'or', markerSize = 3)
				# plt.gca().axis('equal')
				# cbar = plt.colorbar(C1);
				# cbar.add_lines(C2)

		# plt.show()
		# # End debug
		self.eps_a = eps_a
		self.kappa_y = kappa_y
		self.kappa_z = kappa_z
		
	def computeDomainForUltimateConditions(self):

		#material data needed for the computation
		# STEEL
		# ultimate deformation for steel 
		eps_su = self.materials.eps_su
		# yield strength of steel
		fy = self.materials.fy
		# Young modulus
		Es = self.materials.Es

		# ultimate deformation of unconfined concrete
		eps_cu = self.materials.eps_cu
		# peak deformation of unconfined concrete
		eps_cp = self.materials.eps_c
		# peak strength of unconfined concrete
		fc = self.materials.fc
		# ultimate deformation of confined concrete
		eps_ccu = self.materials.eps_ccu
		# peak deformation of confined concrete
		eps_ccp = self.materials.eps_cc
		# peak strength of confined concrete
		fcc = self.materials.fcc
		n = self.materials.n
		
		if self.section is None:
			raise Exception('Error: Section is None')

		# N, My, Mz in OpenSees reference system
		Nlist = []
		Mylist = []
		Mzlist = []
		# numerical integration for obtaining N, Mx, My
		# Create numpy vectors of fibers
		for ea, kx, ky in zip(self.eps_a, self.kappa_y, self.kappa_z):
			N = 0
			Mx = 0
			My = 0
			for group in self.section.surfaceFibers:
				for fiber in group.fibers.fibers:
					# compute epsilon for the fiber
					eps = ea - fiber.x * ky + fiber.y * kx
					sig = paraboRett(fc,eps_cp,eps_cu,n,eps)
					N += sig * fiber.area
					Mx += (sig * fiber.area)* fiber.y
					My += (sig* fiber.area) * (-fiber.x)
			for group in self.section.punctualFibers:
				for fiber in group.fibers.fibers:
					# compute epsilon for the fiber
					eps = ea - fiber.x * ky + fiber.y * kx
					sig = elasticPP(Es,fy,eps_su,eps)
					N += sig * fiber.area
					Mx += (sig * fiber.area)* fiber.y
					My += (sig* fiber.area) * (-fiber.x)
			Nlist.append(N)
			Mylist.append(Mx)
			Mzlist.append(My)
		# # just for debug
		# N = np.array(Nlist)
		# My = np.array(Mylist)
		# Mz = np.array(Mzlist)
		# import mpl_toolkits.mplot3d as a3
		
		# from scipy.spatial import ConvexHull
		# #plt as test the deformation domain
		# ea = np.array(eps_a)
		# ky = np.array(kappa_x)
		# kz = np.array(kappa_y)
		# pts = np.column_stack((ea,ky,kz))
		# hull = ConvexHull(pts)
		# print(hull.points)
		# print(hull.vertices)
		# print(hull.simplices)
		# ax = a3.Axes3D(plt.figure())
		# for s in hull.simplices:
			# plt.plot(pts[s,0], pts[s,1], pts[s,2], 'k-', linewidth = 0.5)
			# tri = a3.art3d.Poly3DCollection([pts[s,:]])
			# tri.set_color((.2,.2,1,0.3))
			# # tri.set_alpha(0.2)
			# ax.add_collection3d(tri)

		# print(len(ea),len(ky),len(kz))
		# ax.scatter(ea, ky, kz)
		# ax.set_xlabel('ea')
		# ax.set_ylabel('ky')
		# ax.set_zlabel('kz')
		
		# # # Alternativelly:
		# # ax = a3.Axes3D(plt.figure())
		
		# # ax.plot_trisurf(hull.points[:,0], hull.points[:,1], hull.points[:,2], triangles = hull.vertices, linewidth=0.2, antialiased=True, color = (.2,.2,1,.3), edgecolor='k')
		# # ax.scatter(ea, ky, kz)
		# # ax.set_xlabel('ea')
		# # ax.set_ylabel('ky')
		# # ax.set_zlabel('kz')
		# # ax.plot_trisurf(x, y, z, triangles=tri.triangles, cmap=plt.cm.Spectral)
		
		# #test convex hull
		# pts = np.column_stack((N,My,Mz))
		# hull = ConvexHull(pts)

		# ax = a3.Axes3D(plt.figure())
		# ax.plot_trisurf(hull.points[:,0], hull.points[:,1], hull.points[:,2], triangles = hull.simplices, linewidth=0.2, antialiased=True, color = (.2,.2,1,.3), edgecolor='k', cmap = plt.cm.Spectral)
		# # ax.plot_trisurf(hull.points[:,0], hull.points[:,1], hull.points[:,2], triangles = hull.simplices, linewidth=0.15, color = (0,0,0,0), edgecolor='k')

		# print(len(N),len(My),len(Mz))
		# ax.scatter(N, My, Mz)

		# ax.set_xlabel('N [N]')
		# ax.set_ylabel('My [Nmm]')
		# ax.set_zlabel('Mz [Nmm]')
		# # plt.show()
		self.N = Nlist
		self.My = Mylist
		self.Mz = Mzlist

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
	if abs(eps) > eps_su:
		return 0
	if eps >= 0:
		sign = 1
	else:
		sign = -1
	sig = sign*min(fy,abs(E*eps))
	return sig
	
	
	
from PySide2.QtCore import (
	QSize,
	)
from PySide2.QtWidgets import (
	QWidget,
	QDialog,
	QGridLayout,
	QLabel,
	QPushButton,
	)
import shiboken2
# import random
	
class DomainResultWidget(QDialog):
	def __init__(self, data, parent = None):
		# base class initialization
		super(DomainResultWidget, self).__init__(parent)
		# layout
		layout = QGridLayout()
		layout.addWidget(QLabel('This is a test Dialog with data: {}'.format(data)),0,0,3,1)
		self.btnClose = QPushButton('Close')
		layout.addWidget(self.btnClose,1,2,1,1)
		
		self.setLayout(layout)
		
		# connections
		self.btnClose.clicked.connect(self.onCloseClicked)

	def onCloseClicked(self):
		self.accept()