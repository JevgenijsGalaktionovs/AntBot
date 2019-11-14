#include <tuple>

#include <ros/ros.h>

#include <stair_estimation.h>
#include <dns/stairs_key.h>

bool stairs_service(dns::stairs_key::Request &req, dns::stairs_key::Response &res){
    if (req.command == true){
        float response[4];
        std::tuple<double, double, double, double> test_reply;
        test_reply = Stairs.getEstimate();
        response[0] = std::get<0>(test_reply);
        response[1] = std::get<1>(test_reply);
        response[2] = std::get<2>(test_reply);
        response[3] = std::get<3>(test_reply);
        for(int i=0; i< 4; i++){
            res.reply.push_back(response[i]);
        }
    }
    return true;
}

int main (int argc, char** argv) try
{
  ros::init (argc, argv, "stair_estimation");
  ros::NodeHandle nh;
  while (ros::ok()){
    ros::ServiceServer service = nh.advertiseService("get_stair_dimensions", stairs_service);
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