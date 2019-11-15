#include <tuple>

#include <ros/ros.h>

#include <stair_estimation.h>
#include <dns/stairs_key.h>

bool get_all_stairs_info_response(dns::stairs_key::Request &req, dns::stairs_key::Response &res){
    if (req.command == true){
        float response[4];
        std::tuple<double, double, double, double> data;
        data = Stairs.getAllEstimates();
        response[0] = std::get<0>(data);
        response[1] = std::get<1>(data);
        response[2] = std::get<2>(data);
        response[3] = std::get<3>(data);
        for(int i=0; i< 4; i++){
            res.reply.push_back(response[i]);
        }
    }
    return true;
}

bool get_stairs_depth_response(dns::stairs_key::Request &req, dns::stairs_key::Response &res){
    res.reply.push_back(Stairs.getDepth());
    return true;
}

bool get_stairs_height_response(dns::stairs_key::Request &req, dns::stairs_key::Response &res){
    res.reply.push_back(Stairs.getHeight());
    return true;
}

bool get_stairs_dist_z_response(dns::stairs_key::Request &req, dns::stairs_key::Response &res){
    res.reply.push_back(Stairs.getDistZ());
    return true;
}

bool get_stairs_dist_x_response(dns::stairs_key::Request &req, dns::stairs_key::Response &res){
    res.reply.push_back(Stairs.getDistX());
    return true;
}

int main (int argc, char** argv) try
{
  ros::init (argc, argv, "stair_estimation");
  ros::NodeHandle nh;
  while (ros::ok()){
    ros::ServiceServer s1 = nh.advertiseService("get_all_stairs_info", get_all_stairs_info_response);
    ros::ServiceServer s2 = nh.advertiseService("get_stairs_depth", get_stairs_depth_response);
    ros::ServiceServer s3 = nh.advertiseService("get_stairs_height", get_stairs_height_response);
    ros::ServiceServer s4 = nh.advertiseService("get_stairs_dist_z", get_stairs_dist_z_response);
    ros::ServiceServer s5 = nh.advertiseService("get_stairs_dist_x", get_stairs_dist_x_response);  

    ros::spin();
  }
  return 0;
}
catch (const rs2::error & e)
{
  std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
  return EXIT_FAILURE;
}
catch (const std::exception & e)
{
  std::cerr << e.what() << std::endl;
  return EXIT_FAILURE;
}