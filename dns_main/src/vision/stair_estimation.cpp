#include <stair_estimation.h>

using St = StairEstimationClass;

bool St::checkFileExists(const std::string& name)
{
  struct stat buffer;
  return (stat (name.c_str(), &buffer) == 0);
}

std::vector<int> St::vectorDifference(std::vector<int> v1, std::vector<int> v2)
{
  std::vector<int> diff;    
  std::set_difference(v1.begin(), v1.end(), v2.begin(), v2.end(),
  std::inserter(diff, diff.begin()));
  // for (auto i : v1) std::cout << i << ' ';
  // std::cout << "minus ";
  // for (auto i : v2) std::cout << i << ' ';
  // std::cout << "is: ";
  // for (auto i : diff) std::cout << i << ' ';
  // std::cout << '\n';
  return diff;
}

template <typename T>
void St::swapTwoVariables(T *xp, T *yp)  
{  
  T temp = *xp;  
  *xp = *yp;  
  *yp = temp;  
}  

int St::openPointCloud(pcl::PointCloud<PointT>::Ptr &input_cloud, char abs_path_string[])
{
  if (pcl::io::loadPCDFile<PointT>(abs_path_string, *input_cloud) == -1){
    return 0;
  }
  if (suppress_prints != true){
    std::cout << "\n";
    std::cout << "Loaded " << input_cloud->width * input_cloud->height  << " points"
              << "(" << input_cloud->width << " x " << input_cloud->height << ")" << "\n";
  }
  return 1;
}

void St::savePointCloud(std::string saveFileName, pcl::PointCloud<PointT>::Ptr &cloud_to_save){
  int i = 0;
  while(checkFileExists(saveFileName + std::to_string(i) + file_format) == true){
    i++;
  }
  if (suppress_prints != true){
    std::cout << "File: " << (saveFileName + std::to_string(i) + file_format) << "\n";
  }
  pcl::io::savePCDFileASCII(saveFileName + std::to_string(i) + file_format, *cloud_to_save); 
}

void St::computePointNormals(pcl::PointCloud<PointT>::Ptr &input_cloud, // Input Point cloud
    pcl::PointCloud<pcl::Normal>::Ptr &output_normals) // Output pointer to store Normals
{
  float max_depth_change = 0.01;
  float smoothing_size = 50.0;
  pcl::IntegralImageNormalEstimation<PointT, pcl::Normal> ne;
  ne.setNormalEstimationMethod(ne.COVARIANCE_MATRIX);
  ne.setMaxDepthChangeFactor(max_depth_change);
  ne.setDepthDependentSmoothing(true);
  ne.setNormalSmoothingSize(smoothing_size);
  ne.setInputCloud(input_cloud);
  ne.compute(*output_normals); 
}

int St::doMultiPlaneSegmentation(
  pcl::PointCloud<PointT>::Ptr        &input_cloud,
  pcl::PointCloud<pcl::Normal>::Ptr   &cloud_normals,
  std::vector<pcl::PlanarRegion<PointT>, Eigen::aligned_allocator<pcl::PlanarRegion<PointT> > > &regions,
  std::vector<pcl::ModelCoefficients> &model_coefficients,
  std::vector<pcl::PointIndices>      &inlier_indices,
  pcl::PointCloud<pcl::Label>::Ptr    &labels,
  std::vector<pcl::PointIndices>      &label_indices,
  std::vector<pcl::PointIndices>      &boundary_indices)
{
  pcl::OrganizedMultiPlaneSegmentation<PointT, pcl::Normal, pcl::Label> seg;
  seg.setInputCloud(input_cloud);
  seg.setInputNormals(cloud_normals);

  unsigned int min_inliers = MIN_INLIERS;
  seg.setMinInliers(min_inliers);
  float angular_thr = ANG_THR_DEG;
  seg.setAngularThreshold(0.01745329 * angular_thr); // 0.01745329 = 1 degree
  float distance_thr = DIST_THR;
  seg.setDistanceThreshold(distance_thr);
  double maximum_curv = MAX_CURV;
  seg.setMaximumCurvature(maximum_curv);
  if (suppress_prints != true){
    std::cout << "\n";
    std::cout << "Segmenting with:\n" 
              << "Minimum Inliers   : " << min_inliers  << "\n"
              << "Angular Threshold : " << angular_thr  << "\n"
              << "Distance Threshold: " << distance_thr << "\n"
              << "Maximum Curvature : " << maximum_curv << "\n"
              << "\n";
  }
  seg.segmentAndRefine(regions, model_coefficients, inlier_indices, labels,
                        label_indices, boundary_indices);

  int found_planes = regions.size();
  if (found_planes == 0){
    if (suppress_prints != true){
      std::cout << "No planes found, please try with different segmentation parameters or take a new pointcloud.\n";
      std::cout << "Terminating the program...\n";
      std::cout << "\n";
    }
    return 1;
  }
  else if (found_planes == 1){
    if (suppress_prints != true){
      std::cout << "Only 1 plane found, please try with different segmentation parameters or take a new pointcloud.\n";
      std::cout << "Terminating the program...\n";
      std::cout << "\n";
    }
    return 2;
  }
  else{
    if (suppress_prints != true){
      std::cout << "Found planes: " << found_planes << "\n";
      std::cout << "\n";
    }
  }  
  return EXIT_SUCCESS;
}

void St::planeBubbleSort(std::vector<int>  &numbers, PointT centroids[],
  std::vector<std::vector<float>> &normals, float p_value[],
  std::vector<pcl::PointIndices> &indices) 
{
  int size = numbers.size();
  int i, j; 
  bool swapped; 
  for (i = 0; i < size-1; i++) 
  { 
    swapped = false; 
    for (j = 0; j < size-i-1; j++){ 
      if (centroids[j].z > centroids[j+1].z) { 


        iter_swap(numbers.begin() + j, numbers.begin() + j+1); // iter_swap for std::vectors.
        iter_swap(normals.begin() + j, normals.begin() + j+1);
        iter_swap(indices.begin() + j, indices.begin() + j+1);
        swapTwoVariables(&centroids[j], &centroids[j+1]); // swap for regular c++ arrays
        swapTwoVariables(&p_value[j], &p_value[j+1]);
        swapped = true; 
      } 
    }
    // IF no two elements were swapped by inner loop, then break 
    if (swapped == false) {break;}
  } 
} 

template <typename T>
double St::dotProduct(T vect_A[], T vect_B[], int size) 
{ 
    double product = 0; 
    for (int i = 0; i < size; i++){
      product = product + (vect_A[i] * vect_B[i]); 
    }
    return product; 
} 

std::tuple<int, int, int> St::RGB_Texture(
  rs2::video_frame texture, rs2::texture_coordinate Texture_XY)
{
  // Get Width and Height coordinates of texture
  int width  = texture.get_width();  // Frame width in pixels
  int height = texture.get_height(); // Frame height in pixels
  
  // Normals to Texture Coordinates conversion
  int x_value = std::min(std::max(int(Texture_XY.u * width  + .5f), 0), width - 1);
  int y_value = std::min(std::max(int(Texture_XY.v * height + .5f), 0), height - 1);

  int bytes = x_value * texture.get_bytes_per_pixel();   // Get # of bytes per pixel
  int strides = y_value * texture.get_stride_in_bytes(); // Get line width in bytes
  int Text_Index =  (bytes + strides);

  const auto New_Texture = reinterpret_cast<const uint8_t*>(texture.get_data());
  
  // RGB components to save in tuple
  int NT1 = New_Texture[Text_Index];
  int NT2 = New_Texture[Text_Index + 1];
  int NT3 = New_Texture[Text_Index + 2];

  return std::tuple<int, int, int>(NT1, NT2, NT3);
}

pcl::PointCloud<PointT>::Ptr St::PCL_Conversion(const rs2::points& points, const rs2::video_frame& color)
{
  pcl::PointCloud<PointT>::Ptr cloud(new pcl::PointCloud<PointT>);
  std::tuple<uint8_t, uint8_t, uint8_t> RGB_Color;

  // Convert data captured from Realsense camera to Point Cloud
  auto sp = points.get_profile().as<rs2::video_stream_profile>();
  
  cloud->width  = static_cast<uint32_t>( sp.width()  );   
  cloud->height = static_cast<uint32_t>( sp.height() );
  cloud->is_dense = false;
  cloud->points.resize( points.size() );

  auto Texture_Coord = points.get_texture_coordinates();
  auto Vertex = points.get_vertices();

  for (int i = 0; i < points.size(); i++)
  {   
    cloud->points[i].x = Vertex[i].x;
    cloud->points[i].y = Vertex[i].y;
    cloud->points[i].z = Vertex[i].z;

    RGB_Color = RGB_Texture(color, Texture_Coord[i]);

    // Mapping Color (BGR due to Camera Model)
    cloud->points[i].r = std::get<2>(RGB_Color); // Reference tuple<2>
    cloud->points[i].g = std::get<1>(RGB_Color); // Reference tuple<1>
    cloud->points[i].b = std::get<0>(RGB_Color); // Reference tuple<0>
  }
  return cloud;
}

void St::flipCoordinateFrame(pcl::PointCloud<PointT>::Ptr &input_cloud)
{
  for(int n = 0; n < input_cloud->width; n++){
    for(int m = 0; m < input_cloud->height; m++){
      PointT in, out;
      in = (*input_cloud)(n,m); // get frame's point
      out.x = -(in.x); // inverting X-axis to flip the image
      out.y = -(in.y); // inverting Y-axis to flip the image
      out.z = in.z;
      (*input_cloud)(n,m) = out;
    }
  }
}

void St::initializeCamera(rs2::pipeline &pipeline)
{
  rs2::align align_to(RS2_STREAM_DEPTH);
  rs2::config cfg; // Create a configuration for configuring the pipeline with a non default profile
  cfg.enable_stream(RS2_STREAM_COLOR,    WIDTH, HEIGHT, RS2_FORMAT_BGR8, FRAMERATE);
  cfg.enable_stream(RS2_STREAM_INFRARED, WIDTH, HEIGHT, RS2_FORMAT_Y8,   FRAMERATE);
  cfg.enable_stream(RS2_STREAM_DEPTH,    WIDTH, HEIGHT, RS2_FORMAT_Z16,  FRAMERATE);
  rs2::pipeline_profile selection = pipeline.start(cfg); 
  rs2::device selected_device = selection.get_device();
  auto depth_sensor = selected_device.first<rs2::depth_sensor>();

  if (depth_sensor.supports(RS2_OPTION_EMITTER_ENABLED)){
    depth_sensor.set_option(RS2_OPTION_EMITTER_ENABLED, 1.f); // Enable emitter
    depth_sensor.set_option(RS2_OPTION_EMITTER_ENABLED, 0.f); // Disable emitter
  }
  if (depth_sensor.supports(RS2_OPTION_LASER_POWER)){
    // Query min and max values:
    rs2::option_range range = depth_sensor.get_option_range(RS2_OPTION_LASER_POWER);
    depth_sensor.set_option(RS2_OPTION_LASER_POWER, range.max); // Set max power
    depth_sensor.set_option(RS2_OPTION_LASER_POWER, 0.f); // Disable laser
  }

  // Drop several frames for auto-exposure
  for (int i = 0; i < 30; i++) {
    auto frames = pipeline.wait_for_frames(); 
  }

}

void St::applyFilters(rs2::frame &depth)
{
  rs2::threshold_filter thr_filter;
  thr_filter.set_option(RS2_OPTION_MIN_DISTANCE, 0.35); // 35cm from camera MIN
  thr_filter.set_option(RS2_OPTION_MAX_DISTANCE, 3.0); // 3m from camera MAX
  depth = thr_filter.process(depth);

  rs2::decimation_filter dec_filter;
  dec_filter.set_option(RS2_OPTION_FILTER_MAGNITUDE, 2);
  depth = dec_filter.process(depth);

  rs2::disparity_transform depth2disparity;
  depth = depth2disparity.process(depth);


  rs2::spatial_filter spat_filter;
  spat_filter.set_option(RS2_OPTION_FILTER_MAGNITUDE, 2); // 2 def. Number of filter iterations 	[1-5]
  spat_filter.set_option(RS2_OPTION_FILTER_SMOOTH_ALPHA, 0.25); // 0.5 def.Exponential moving average factor. 1 = no filter,0 = infinite filter [0.25-1]
  spat_filter.set_option(RS2_OPTION_FILTER_SMOOTH_DELTA, 8); // 20 def. Step-size boundary. Threshold used to preserve edges [1-50]
  spat_filter.set_option(RS2_OPTION_HOLES_FILL, 4); // 0 def. Filling holes. [0-5] range mapped to [none,2,4,8,16,unlimited] pixels.
  depth = spat_filter.process(depth);

  
  rs2::temporal_filter temp_filter;
  temp_filter.set_option(RS2_OPTION_FILTER_SMOOTH_ALPHA, 0.6); // 0.4 def.Exponential moving average factor. 1 = no filter,0 = infinite filter [0.25-1]
  temp_filter.set_option(RS2_OPTION_FILTER_SMOOTH_DELTA, 10); // 20 def. Step-size boundary. Threshold used to preserve edges [1-50]
  // temp_filter.set_option(R ,2); // 2 def. Number of filter iterations 	[1-5]
  depth = temp_filter.process(depth);

  rs2::disparity_transform disparity2depth(false);
  depth = disparity2depth.process(depth);

  // rs2::hole_filling_filter hole_filter;
  // hole_filter.set_option(RS2_OPTION_HOLES_FILL, 1); // [0-2] enumerated: fill_from_left - farest_from_around - nearest_from_around 
  // depth = hole_filter.process(depth);
}

void St::getFreshCloud(rs2::pipeline &pipe, pcl::PointCloud<PointT>::Ptr &input_cloud)
{
  rs2::pointcloud pointcloud;
  rs2::points points;
  rs2::frameset frames = pipe.wait_for_frames();
  rs2::depth_frame depth = frames.get_depth_frame();
  rs2::video_frame RGB = frames.get_color_frame();
  pointcloud.map_to(RGB);

  applyFilters(depth);

  points = pointcloud.calculate(depth); // Generate Point Cloud
  input_cloud = PCL_Conversion(points, RGB);

  if (save_raw == true){
    savePointCloud(name_raw, input_cloud);
  }
}

int St::updateSavedPlanes(std::vector<int> &saved_pl_Numbers,
  PointT saved_pl_Centroids[],
  float saved_pl_PValue[],
  std::vector<pcl::PointIndices> &saved_pl_Indices,
  std::vector<std::vector<float>> &saved_pl_Normals,
  PointT pl_Centroids[],
  float pl_PValue[],
  std::vector<pcl::PointIndices> &inlier_indices,
  std::vector<std::vector<float>> &pl_Normals  
  )
{

  int numSavedPlanes = saved_pl_Numbers.size();

  if (numSavedPlanes == 0){
    if (suppress_prints != true){
      std::cout << "No planes saved, please try with different segmentation parameters or take a new pointcloud.\n";
      std::cout << "Terminating the program...\n";
      std::cout << "\n";
    }
    return 3;
  }
  else if (numSavedPlanes == 1){
    if (suppress_prints != true){
      std::cout << "Only 1 plane saved. Minimum number of planes to compute distance = 2.\n";
      std::cout <<  "Please try with different segmentation parameters or take a new pointcloud.\n";
      std::cout << "Terminating the program...\n";
      std::cout << "\n";
    }
    return 4;
  }
  if (suppress_prints != true){
    std::cout << "\n";
    std::cout << "Saved Planes ID: ";
    for (int i = 0; i < numSavedPlanes; i++){

      std::cout << saved_pl_Numbers[i] << " ";
    }
    std::cout << "\n";
  }

  // Updating Saved data from original data.
  for (int v = 0; v < numSavedPlanes; v++){
    saved_pl_Centroids[v] = pl_Centroids[saved_pl_Numbers[v]];
    saved_pl_Normals[v]   = pl_Normals[saved_pl_Numbers[v]];
    saved_pl_PValue[v]    = pl_PValue[saved_pl_Numbers[v]];
    saved_pl_Indices[v]   = inlier_indices[saved_pl_Numbers[v]];
  }
  return EXIT_SUCCESS;
}

int St::computeStairDimensions(std::vector<std::vector<float>> &saved_pl_Normals, PointT saved_pl_Centroids[])
{
  int numSavedPlanes = saved_pl_Normals.size();
  int plane_index = 0;
  for( int i = 0; i < numSavedPlanes;i++){
    if ((saved_pl_Centroids[plane_index + 1].z - saved_pl_Centroids[plane_index].z) < 0.05){
      plane_index++;
    }
    else{ break; }
  }

  if(plane_index >= numSavedPlanes){
    if (suppress_prints != true){
      std::cout << "None of the planes is farther than 5cm from each other.\n ";
    }
    return 5;
  }

  double N[3] = {-saved_pl_Normals[plane_index][0], -saved_pl_Normals[plane_index][1], -saved_pl_Normals[plane_index][2]};
  double step1[3] = {saved_pl_Centroids[plane_index].x, saved_pl_Centroids[plane_index].y, saved_pl_Centroids[plane_index].z};
  double step2[3] = {saved_pl_Centroids[plane_index+1].x, saved_pl_Centroids[plane_index+1].y, saved_pl_Centroids[plane_index+1].z};
  double step_diff[3];
  for(int i = 0; i < 3; i++){
    step_diff[i] = (step2[i]*100) - (step1[i]*100);
  }
  // Output units : millimeters
  step_depth_withEq = (dotProduct(step_diff, N, 3)) * 10;
  step_depth_noEq =(step2[2] - step1[2]) * 1000;
  step_height = (step2[1] - step1[1]) * 1000;
  dist_z_to_1step = (saved_pl_Centroids[0].z) * 1000;
  dist_x_to_1step = (saved_pl_Centroids[0].x) * 1000;  

  if (suppress_prints != true){
    std::cout << "Step Depth  is " << step_depth_withEq << "cm. With Equation.\n";
    std::cout << "Step Depth  is " << step_depth_noEq   << "cm. Without Equation.\n";
    std::cout << "Step Height is " << step_height       << "cm. \n";
    std::cout << "Z Distance to first step is " << dist_z_to_1step   << "cm.\n";
    std::cout << "X Distance to first step is " << dist_x_to_1step   << "cm.\n";
  }
  return EXIT_SUCCESS;
}

void St::findPlaneData(int &num_found_planes, std::vector<int> &planeNrToDelete,
  PointT pl_centroids[],
  std::vector<std::vector<float>> & pl_normals,
  float pl_pvalues[],
  std::vector<pcl::PlanarRegion<PointT>, Eigen::aligned_allocator<pcl::PlanarRegion<PointT> > > &regions,
  std::vector<pcl::ModelCoefficients> &model_coefficients)
{
  int planeCount = 0;
  for(int i = 0; i < num_found_planes; i++){
    Eigen::Vector3f centroid = regions[i].getCentroid();
    pl_centroids[i].x = centroid[0];
    pl_centroids[i].y = centroid[1];
    pl_centroids[i].z = centroid[2];
    pl_normals[i][0] = model_coefficients[i].values[0];
    pl_normals[i][1] = model_coefficients[i].values[1];
    pl_normals[i][2] = model_coefficients[i].values[2];
    pl_pvalues[i]     = model_coefficients[i].values[3];


    
    // Plane filtering
    if (pl_centroids[i].x > 0.5 || pl_centroids[i].x < -0.5 
      || pl_centroids[i].y > 1.5 || pl_centroids[i].z > 1.5 
      || pl_normals[i][0] > 0.5 || pl_normals[i][0] < -0.5
      || pl_normals[i][1] > 0.8 || pl_normals[i][1] < -0.8)        
    {
      planeNrToDelete[planeCount] = i;
      if (suppress_prints != true){
        std::cout << "(REMOVED)";
      }
      planeCount++;
    } 
    if (suppress_prints != true){
      std::cout << "Plane " << i << ": "  << (double)regions[i].getCount() <<" Inliers."
                << " Centroid: (" << pl_centroids[i].x << ", " <<  pl_centroids[i].y << ", " <<  pl_centroids[i].z << "); "
                << "Normal: (" << pl_normals[i][0] << ", " << pl_normals[i][1] << ", " << pl_normals[i][2] << ")." << "\n";
    }
  }
}


int St::doEstimate()
{
  int status;
  pcl::PointCloud<PointT>::Ptr cloud (new pcl::PointCloud<PointT>);

  // TEMPORARY
  // char* open_cloud = "/home/eugeneswag/ros_workspace/src/DNS/dns_main/src/vision/pcd/raw_cloud3.pcd";
  // openPointCloud(cloud,open_cloud);
  getFreshCloud(pipe, cloud);

  flipCoordinateFrame(cloud);

  pcl::PointCloud<pcl::Normal>::Ptr cloud_normals (new pcl::PointCloud<pcl::Normal>);
  computePointNormals(cloud, cloud_normals);

  std::vector<pcl::PlanarRegion<PointT>, Eigen::aligned_allocator<pcl::PlanarRegion<PointT> > > regions;
  std::vector<pcl::ModelCoefficients> model_coefficients;
  std::vector<pcl::PointIndices>      inlier_indices;
  pcl::PointCloud<pcl::Label>::Ptr    labels(new pcl::PointCloud<pcl::Label>);
  std::vector<pcl::PointIndices>      label_indices;
  std::vector<pcl::PointIndices>      boundary_indices;
  status = doMultiPlaneSegmentation(cloud, cloud_normals, regions, model_coefficients, inlier_indices,
    labels, label_indices, boundary_indices);
  if (status==1){
    return 1;
  }
  else if(status==2){
    return 2;
  }

  int numFoundPlanes = regions.size();
  PointT pl_Centroids[numFoundPlanes];
  float  pl_PValue[numFoundPlanes];
  std::vector<std::vector<float>> pl_Normals(numFoundPlanes, std::vector<float>(3, 0));
  std::vector<int> planeNrFound(numFoundPlanes);
  for (int e = 0; e < numFoundPlanes; e++){ planeNrFound[e] = e; }
  std::vector<int> planeNrToDelete(numFoundPlanes, 1234); // 1234 <- value to initialize vector. Must not be equal to possible plane numbers e.g 0-100
  findPlaneData(numFoundPlanes, planeNrToDelete, pl_Centroids, pl_Normals, pl_PValue, regions, model_coefficients);

  std::vector<int> saved_pl_Numbers;
  saved_pl_Numbers = vectorDifference(planeNrFound,planeNrToDelete);
  int numSavedPlanes = saved_pl_Numbers.size();
  PointT saved_pl_Centroids[numSavedPlanes];
  float saved_pl_PValue[numSavedPlanes];
  std::vector<pcl::PointIndices> saved_pl_Indices(numSavedPlanes);
  std::vector<std::vector<float>> saved_pl_Normals(numSavedPlanes, std::vector<float>(3, 0));
  status = updateSavedPlanes(saved_pl_Numbers,saved_pl_Centroids, saved_pl_PValue, saved_pl_Indices, saved_pl_Normals,
    pl_Centroids,pl_PValue, inlier_indices, pl_Normals);
  if (status==3){
    return 3;
  }
  else if(status==4){
    return 4;
  }
  // Ordering all Plane data as follows: plane closest to camera (Z-axis) is first, next closest is 2nd and so on...
  planeBubbleSort(saved_pl_Numbers, saved_pl_Centroids, saved_pl_Normals, saved_pl_PValue, saved_pl_Indices);


  status = computeStairDimensions(saved_pl_Normals, saved_pl_Centroids);
  if (status==5){
    return 5;
  }

  pcl::copyPointCloud(*cloud, saved_pl_Indices, *cloud); // only saved planes
  if(save_filtered == true){
    savePointCloud(name_filtered, cloud);
  }

  return EXIT_SUCCESS;
}

std::string status_check(int status){
    std::string status_text;
    if (status==1){
      status_text = "Segmentation fail -> No planes found.";
    }
    else if (status==2){
      status_text = "Segmentation fail -> Only 1 plane found (Must be at least 2).";
    }
    else if (status==3){
      status_text = "Filtering -> No good planes found.";
    }
    else if (status==4){
      status_text = "Filtering -> Only 1 good plane found.";
    }
    else if (status==5){
      status_text = "Dimensions -> None of the planes is farther than 5cm from each other.";
    }
    else{
      status_text = "Something weird happened... Only god knows.";
    }
    return status_text;
}

std::tuple<double, double, double, double> St::getAllEstimates(){
  std::string status_msg;
  int status = doEstimate();
  
  if(status == EXIT_SUCCESS){
    return std::tuple<double, double, double, double>(step_depth_noEq, step_height, dist_z_to_1step, dist_x_to_1step);
  }
  else{
    status_msg = status_check(status);
    if (suppress_prints != true){
      std::cout << status_msg << "\n";
    }
    return std::tuple<double, double, double, double>(0, 0, 0, 0);
  }
}

double St::getDepth(){
  std::string status_msg;
  int status = doEstimate();
  
  if(status == EXIT_SUCCESS){
    return step_depth_noEq;
  }
  else{
    status_msg = status_check(status);
    if (suppress_prints != true){
      std::cout << status_msg << "\n";
    }
    return 0;
  }
}

double St::getHeight(){
  std::string status_msg;
  int status = doEstimate();
  
  if(status == EXIT_SUCCESS){
    return step_height;
  }
  else{
    status_msg = status_check(status);
    if (suppress_prints != true){
      std::cout << status_msg << "\n";
    }
    return 0;
  }
}

double St::getDistZ(){
  std::string status_msg;
  int status = doEstimate();
  
  if(status == EXIT_SUCCESS){
    return dist_z_to_1step;
  }
  else{
    status_msg = status_check(status);
    if (suppress_prints != true){
      std::cout << status_msg << "\n";
    }
    return 0;
  }
}

double St::getDistX(){
  std::string status_msg;
  int status = doEstimate();
  
  if(status == EXIT_SUCCESS){
    return dist_x_to_1step;
  }
  else{
    status_msg = status_check(status);
    if (suppress_prints != true){
      std::cout << status_msg << "\n";
    }
    return 0;
  }
}

St Stairs;