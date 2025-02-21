import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
    
    # factor
    at_factor = MpcAttributeMetaData()
    at_factor.type = MpcAttributeType.Real
    at_factor.name = 'factor'
    at_factor.group = '-ThermalBoundaryConditionTemperature'
    at_factor.setDefault(1.0)
    at_factor.description = (
        html_par(html_begin()) +
        html_par(html_boldtext('factor')+'<br/>') +
        html_par('factor to apply to temperature setting') +
        html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/EleLoad_Command','EleLoad Command')+'<br/>') +
        html_end()
        )
    
    xom = MpcXObjectMetaData()
    xom.name = 'eleLoad_ThermalBoundaryConditionTemperature'

    xom.addAttribute(at_factor)
    
    
    return xom

def fillConditionRepresentationData(xobj, pos, data):
    '''
    Fills the 3D vector data.
    
    Set the pressure value
    at the z component, since the orientation is set to local
    '''
    # Dimension = xobj.getAttribute('Dimension').string
    # use_Wx = xobj.getAttribute('use_Wx').boolean
    # Wx = xobj.getAttribute('Wx').real
    # Wy = xobj.getAttribute('Wy').real
    # Wz = xobj.getAttribute('Wz').real
    
    # if not use_Wx:
    #     Wx = 0
    
    # if (Dimension == '2D'):
    #     data[0] = Wx
    #     data[1] = Wy
    #     data[2] = 0
    
    # else:
    #     data[0] = Wx
    #     data[1] = Wy
    #     data[2] = Wz

def makeConditionRepresentationData(xobj):
    '''
    Create the condition representation data for STKO.
    Here we want an arrow (vector) representation in local
    coordinate system, that can be applied only on faces.
    We need to allocate a 3d vector for the data attribute.
    The components of this vector will be set using
    @ref fillConditionRepresentationData
    '''
    d = MpcConditionRepresentationData()
    d.type = MpcConditionVRepType.Points
    d.orientation = MpcConditionVRepOrientation.Global
    d.data = Math.double_array([0.0, 0.0, 0.0])
    d.on_vertices = False
    d.on_edges = False
    d.on_faces = True
    d.on_solids = False
    d.on_interactions = False
    return d

def writeTcl_eleLoad(pinfo, xobj):
    
    # 2D
    # eleLoad -ele $eleTag1 <$eleTag2 ....> -type -beamUniform $Wy <$Wx>
    
    # 3D
    # eleLoad -ele $eleTag1 <$eleTag2 ....> -type -beamUniform $Wy $Wz <$Wx>
    
    ClassName = xobj.name
    if pinfo.currentDescription != ClassName:
        pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
        pinfo.currentDescription = ClassName
    
    tag = xobj.parent.componentId
    
    all_geom = pinfo.condition.assignment.geometries
    if len(all_geom) == 0:
        return
    
    sopt = ''
    
    
    factor_at = xobj.getAttribute('factor')
    if(factor_at is None):
        raise Exception('Error: cannot find "factor" attribute')
    factor = factor_at.real
    
    
    doc = App.caeDocument()
    
    is_partitioned = False
    if pinfo.process_count > 1:
        is_partitioned = True
    if is_partitioned:
        raise Exception("Partitioned analysis unsupported yet for eleLoad_ThermalBoundaryConditionTemperature.py")
        # process_block_count = 0
        # for process_id in range(pinfo.process_count):
        #     first_done = False
            
        #     if not is_Global:
        #         #is in local system
        #         for geom, item in all_geom.items():
        #             mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
        #             domain_collection = mesh_of_geom.edges
        #             eleTag = ''
        #             for i in item.edges:
        #                 domain = domain_collection[i]
        #                 for element in domain.elements:
        #                     if doc.mesh.partitionData.elementPartition(element.id)!= process_id:
        #                         continue
        #                     if not first_done:
        #                         if process_block_count == 0:
        #                             pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
        #                         else:
        #                             pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
        #                         first_done = True
                            
        #                     eleTag += ' {}'.format(element.id)
        #             if eleTag:
        #                 str_tcl = '{}eleLoad -ele{} -type -beamUniform {}{}\n'.format(pinfo.indent, eleTag, Wy, sopt)
                        
        #                 # now write the string into the file
        #                 pinfo.out_file.write(str_tcl)
        #         if is_partitioned :
        #             if first_done:
        #                 process_block_count += 1
        #             if process_block_count > 0 and first_done:
        #                 pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
        #     else:
        #         # is in global system
        #         for geom, item in all_geom.items():
        #             mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
        #             domain_collection = mesh_of_geom.edges
        #             for i in item.edges:
        #                 domain = domain_collection[i]
        #                 str_tcl = []
        #                 for element in domain.elements:
        #                     if doc.mesh.partitionData.elementPartition(element.id)!= process_id:
        #                         continue
        #                     if not first_done:
        #                         if process_block_count == 0:
        #                             pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
        #                         else:
        #                             pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
        #                         first_done = True
        #                     WT = element.orientation.quaternion.conjugate().rotate(W)
        #                     if Dimension_3D:
        #                         str_tcl.append('{}eleLoad -ele {} -type -beamUniform {} {} {}'.format(pinfo.indent, element.id, WT.y, WT.z, WT.x))
        #                     else:
        #                         str_tcl.append('{}eleLoad -ele {} -type -beamUniform {} {} {}'.format(pinfo.indent, element.id, WT.y, WT.x))
        #                 # now write the string into the file
        #                 if len(str_tcl) > 0:
        #                     pinfo.out_file.write('\n'.join(str_tcl))
        #                     pinfo.out_file.write('\n')
        #         if is_partitioned :
        #             if first_done:
        #                 process_block_count += 1
        #             if process_block_count > 0 and first_done:
        #                 pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
            
    else:
        # is in local system
        for geom, item in all_geom.items():
            mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
            domain_collection = mesh_of_geom.faces
            eleTag = ''
            for i in item.faces:
                domain = domain_collection[i]
                for element in domain.elements:
                    eleTag += ' {}'.format(element.id)
                
            str_tcl = '{}eleLoad -ele{} -type -ThermalBoundaryConditionTemperature {}\n'.format(pinfo.indent, eleTag, factor)
            
            # now write the string into the file
            pinfo.out_file.write(str_tcl)
