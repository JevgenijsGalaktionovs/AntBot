#ifndef stair_estimation_h
#define stair_estimation_h

#include <iostream>
#include <string>
#include <tuple>
#include <sys/stat.h> // For checkFileExists method

#include <ros/ros.h>
#include <librealsense2/rs.hpp>

#include <pcl/common/common_headers.h>
#include <pcl/io/pcd_io.h>
#include <pcl/segmentation/organized_multi_plane_segmentation.h>
#include <pcl/features/integral_image_normal.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/point_types.h>

// Best recommended resolution by Intel technologies (D435 camera)
#define WIDTH        848
#define HEIGHT       480 
#define FRAMERATE    30

// Segmentation parameters
#define MIN_INLIERS   1000
#define ANG_THR_DEG   3
#define DIST_THR      0.05
#define MAX_CURV      0.01

#define SAVE_RAW false
#define SAVE_FLT false
#define SUPPRESS_PRINTS false

using PointT =  pcl::PointXYZRGB;

class StairEstimationClass {
public:
  // Constructor
  StairEstimationClass(): save_raw(SAVE_RAW), save_filtered(SAVE_FLT), suppress_prints(SUPPRESS_PRINTS) {
    initializeCamera(pipe);
  }

  // Public Members
  bool save_raw;
  bool save_filtered;
  bool suppress_prints;
  std::string file_format   = ".pcd";
  std::string name_raw      = "/home/eugeneswag/ros_workspace/src/DNS/dns_main/src/vision/pcd/raw_cloud";
  std::string name_filtered = "/home/eugeneswag/ros_workspace/src/DNS/dns_main/src/vision/pcd/filtered_cloud";

  double step_height, step_depth_withEq, step_depth_noEq, dist_z_to_1step, dist_x_to_1step;

  // Public Methods
  std::tuple<double, double, double, double> getAllEstimates();
  double getDepth();
  double getHeight();
  double getDistZ();
  double getDistX();


  template <typename T>
  void swapTwoVariables(T *xp, T *yp);
  template <typename T>
  double dotProduct(T vect_A[], T vect_B[], int size);
  bool checkFileExists(const std::string& name);
  std::vector<int> vectorDifference(std::vector<int> v1, std::vector<int> v2);


private:
  // Private Members
  rs2::pipeline pipe; // RealSense pipeline, encapsulating the actual device and sensors

  // Private Methods
  void initializeCamera(rs2::pipeline &pipeline);
  int doEstimate();
  int updateSavedPlanes(std::vector<int> &saved_pl_Numbers,
    PointT saved_pl_Centroids[],
    float saved_pl_PValue[],
    std::vector<pcl::PointIndices> &saved_pl_Indices,
    std::vector<std::vector<float>> &saved_pl_Normals,
    PointT pl_Centroids[],
    float pl_PValue[],
    std::vector<pcl::PointIndices> &inlier_indices,
    std::vector<std::vector<float>> &pl_Normals);
  void flipCoordinateFrame(pcl::PointCloud<PointT>::Ptr &input_cloud);
  void getFreshCloud(rs2::pipeline &pipe, pcl::PointCloud<PointT>::Ptr &input_cloud);
  void applyFilters(rs2::frame &depth);
  int computeStairDimensions(std::vector<std::vector<float>> &saved_pl_Normals, PointT saved_pl_Centroids[]);
  void findPlaneData(int &num_found_planes, std::vector<int> &planeNrToDelete,
    PointT pl_centroids[],
    std::vector<std::vector<float>> & pl_normals,
    float pl_pvalues[],
    std::vector<pcl::PlanarRegion<PointT>, Eigen::aligned_allocator<pcl::PlanarRegion<PointT> > > &regions,
    std::vector<pcl::ModelCoefficients> &model_coefficients);
  void computePointNormals(pcl::PointCloud<PointT>::Ptr &input_cloud, // Input Point cloud
      pcl::PointCloud<pcl::Normal>::Ptr &output_normals); // Output pointer to store Normals
  int doMultiPlaneSegmentation(
    pcl::PointCloud<PointT>::Ptr        &input_cloud,
    pcl::PointCloud<pcl::Normal>::Ptr   &cloud_normals,
    std::vector<pcl::PlanarRegion<PointT>, Eigen::aligned_allocator<pcl::PlanarRegion<PointT> > > &regions,
    std::vector<pcl::ModelCoefficients> &model_coefficients,
    std::vector<pcl::PointIndices>      &inlier_indices,
    pcl::PointCloud<pcl::Label>::Ptr    &labels,
    std::vector<pcl::PointIndices>      &label_indices,
    std::vector<pcl::PointIndices>      &boundary_indices);

  void planeBubbleSort(std::vector<int>  &numbers, PointT centroids[],
    std::vector<std::vector<float>> &normals, float p_value[],
    std::vector<pcl::PointIndices> &indices);

  std::tuple<int, int, int> RGB_Texture(
    rs2::video_frame texture, rs2::texture_coordinate Texture_XY);

  pcl::PointCloud<PointT>::Ptr PCL_Conversion(const rs2::points& points, const rs2::video_frame& color);
  int openPointCloud(pcl::PointCloud<PointT>::Ptr &input_cloud, char abs_path_string[]);
  void savePointCloud(std::string saveFileName, pcl::PointCloud<PointT>::Ptr &cloud_to_save);
};

extern StairEstimationClass Stairs;
#endif