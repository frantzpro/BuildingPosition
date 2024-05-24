FROM ros:noetic
SHELL ["/bin/bash", "-c"]

ENV semantix_port=7500
ENV xmlrpc_port=45100
ENV tcpros_port=45101
ENV DEBIAN_FRONTEND=noninteractive
#ENV ROS_IP=127.0.0.1
#ENV ROS_MASTER_URI=http://127.0.0.1:11311
ENV USE_ENV_ROS_MASTER_URI=True

EXPOSE 3883

#ENV ROS_MASTER_URI=http://172.20.34.240:11311
#ENV ROS_IP=172.20.34.240

# ROS-Noetic Setup
RUN sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-get update && apt-get install -y curl
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

RUN sudo apt-get update
RUN apt-get update && apt-get install -y python3-rosinstall python3-rosinstall-generator python3-wstool build-essential python3-rosdep python3-catkin-tools ros-noetic-vrpn-client-ros
#Install required kobuki packages, no included in standard install
RUN apt-get update && apt-get install -y  ros-noetic-control-toolbox ros-noetic-tf ros-noetic-cv-bridge
RUN apt-get update && apt-get install -y python-is-python3 python3-pip git iputils-ping liborocos-kdl-dev

#RUN sudo /ros_ws/src/mavros/mavros/scripts/install_geographiclib_datasets.sh
RUN rosdep update
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
RUN source ~/.bashrc

# Add Files
ADD ros_ws /ros_ws
COPY protocols /etc

COPY /ViconPosition.py /ros_ws/src/building_positions
COPY /AbstractVirtualCapability.py /ros_ws/src/building_positions
COPY /requirements /var

#RUN cd ros_ws && source /opt/ros/noetic/setup.bash && rosdep install --from-paths . --ignore-src -r -y
RUN cd /ros_ws && source /opt/ros/noetic/setup.bash && catkin build

RUN source /ros_ws/devel/setup.bash

#Setup Env
ENTRYPOINT ["/ros_entrypoint.sh"]

CMD source /ros_ws/devel/setup.bash && roslaunch building_positions building_positions.launch semantix_port:=${semantix_port}
