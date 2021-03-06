#!/usr/bin/env python3

# Code copied from main depthai repo, depthai_helpers/projector_3d.py

import numpy as np
import open3d as o3d

class PointCloudVisualizer():
    def __init__(self, intrinsic_matrix, width, height):
        self.depth_map = None
        self.rgb = None
        self.pcl = None
        self.d = 0
        self.pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(width,
                                                                         height,
                                                                         intrinsic_matrix[0][0],
                                                                         intrinsic_matrix[1][1],
                                                                         intrinsic_matrix[0][2],
                                                                         intrinsic_matrix[1][2])
        # Added to code by CALGARY_STORM.
        # This will flip the view in the display so that it's on inverted
        self.flip_transform = [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
        
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.isstarted = False

    def rgbd_to_projection(self, depth_map, rgb, is_rgb):
        self.depth_map = depth_map
        self.rgb = rgb
        rgb_o3d = o3d.geometry.Image(self.rgb)
        depth_o3d = o3d.geometry.Image(self.depth_map)
        # TODO: query frame shape to get this, and remove the param 'is_rgb'
        if is_rgb:
            rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(rgb_o3d, depth_o3d, convert_rgb_to_intensity=False)
        else:
            rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(rgb_o3d, depth_o3d)
        if self.pcl is None:
            self.pcl = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, self.pinhole_camera_intrinsic)
        else:            
            pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, self.pinhole_camera_intrinsic)
            self.pcl.points = pcd.points
            self.pcl.colors = pcd.colors
        return self.pcl

    def visualize_pcd(self):
        if not self.isstarted:
            # Code added by CALGARY_STORM. Code flips the 3D image so that it 
            # displays correctly, otherwise image displays inverted, and you 
            # will need to manually invert the picture
            self.pcl.transform(self.flip_transform)
            self.vis.add_geometry(self.pcl)
            # TODO: DELETE THE COMMENTED OUT CODE (CALGARY_STORM)
            # THIS CODE CREATES A 3D AXIS, RED, GREEN, BLUE. 
            #origin = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.3, origin=[0, 0, 0])
            #self.vis.add_geometry(origin)
            self.vis.add_geometry(self.pcl)
            self.isstarted = True
        else:
            # Code added by CALGARY_STORM. Code flips the 3D image so that it 
            # displays correctly, otherwise image displays inverted, and you 
            # will need to manually invert the picture
            self.pcl.transform(self.flip_transform)
            self.vis.update_geometry(self.pcl)
            self.vis.poll_events()
            self.vis.update_renderer()
            # Save path
            d = self.d
            pcd_save_path = './PCD_save_files/pcd_%04d.pcd'%d
            # Write the pcd to save file
            o3d.io.write_point_cloud(pcd_save_path, self.pcl)
            self.d += 1
           

    def close_window(self):
        self.vis.destroy_window()
