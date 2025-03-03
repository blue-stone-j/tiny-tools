# first argument: folder name
# second argument: package type

# create a folder with the following structure:
# folder
# ├── third_party
# ├── assets
# ├── build
# ├── cmake
# │   ├── global_definition.cmake
# │   └── folderConfig.cmake.in
# ├── component
# ├── config
# │   └── config.json
# ├── core
# ├── debian
# │   └── control
# │   └── rules
# │   └── changelog
# │   └── compat
# ├── include
# │   └── global_definition.h.in
# ├── install
# └── plugin
# ├── src
# ├── test
# ├── cbuild.sh
# ├── CMakeLists.txt


# Check if a folder name is provided
if [ -z "$1" ]; then
  echo "Usage: create_folder <folder_name>"
  exit 1
fi

name=$1
# translates all lowercase letters to uppercase
name_upper=$(echo "$1" | tr '[:lower:]' '[:upper:]')

if [ -z "$2" ]; then
  echo "unspecified package type: should be 'lib' or 'app'"
  type=""
else
  type=$2
fi

# Create the folder
mkdir -p "$name"
echo "Folder '$name' created successfully."

cd $name

# create subfolders
mkdir -p third_party
mkdir -p assets
mkdir -p build
mkdir -p cmake
mkdir -p component
mkdir -p config
mkdir -p install
mkdir -p scripts

if [ "$type" == "lib" ]; then
  mkdir -p include
  mkdir -p src
  mkdir -p test
elif [ "$type" == "app" ]; then
  mkdir -p core
  mkdir -p plugin
fi

# create config
cd config
touch config.json

# create Config.cmake.in
cd ../cmake

if [ "$type" == "lib" ]; then
  cat <<EOF > $name"Config.cmake.in"
set(\${PROJECT_NAME}_INCLUDE_DIRS "")
list(APPEND \${PROJECT_NAME}_INCLUDE_DIRS
  \${CMAKE_INSTALL_PREFIX}/include)

file(GLOB_RECURSE \${PROJECT_NAME}_LIBRARIES
  \${CMAKE_INSTALL_PREFIX}/lib/\${PROJECT_NAME}/*.so)
EOF
elif [ "$type" == "app" ]; then
  # create debian
  mkdir -p debian

fi

cat <<EOF > "global_definition.cmake"
set(SOFTWARE_VERSION \${${name_upper}_VERSION})

string(TIMESTAMP RELEASE_DATE "%d.%m.%y")

if(_WIN_)
  set(SYSTEM_VERSION Windows)
elseif(UNIX AND NOT APPLE)
  set(SYSTEM_VERSION Linux)
elseif(APPLE)
  set(SYSTEM_VERSION macOS)
else()
  set(SYSTEM_VERSION Unknow)
endif()

configure_file(
  \${CMAKE_CURRENT_SOURCE_DIR}/include/global_definition.h.in
  \${CMAKE_CURRENT_SOURCE_DIR}/include/global_definition.h
)

EOF

# create global_definition.h.in
cd ../include
cat <<EOF > "global_definition.h.in"
#ifndef GLOBAL_DEFINITION_H
#define GLOBAL_DEFINITION_H

#include <string>

const std::string SYSTEM_VERSION="@SYSTEM_VERSION@";
const std::string SOFTWARE_VERSION="@SYSTEM_VERSION@";
const std::string RELEASE_DATE="@RELEASE_DATE@";

#if defined(_WIN32) || defined(_WIN64)
#include <windows.h>
#include <vector>
static std::string getExePath()
{
  char result[MAX_PATH];
  GeModuleFileName(NULL, result, MAX_PATH);
  return std::string(result);
}
#elif defined(__linux__)
#include <unistd.h>
static std::string getExePath()
{
  constexpr int len = 256;
  char arr_tmp[len] = {0};

  int n = readlink("/proc/self/exe", arr_tmp, len);
  if (n >= len || n == -1)
  {
    // LOG(WARNING) << "Failed to read the executable path";
    return "";
  }

  std::string exePath(arr_tmp, n);
  std::string::size_type pos = exePath.find_last_of('/');
  if (pos == std::string::npos)
  {
    return "";
  }
  return exePath;
}
#endif

static std::string getExeDir()
{
  return std::filesystem::path(getExePath()).parent_path().string();
}

static std::string getRootDir()
{
  return std::filesystem::path(getExeDir()).parent_path().string();
}
const std::string WORK_SPACE_PATH = getRootDir();

#endif

EOF


# create CMakeLists.txt
cd ..
cat <<EOF > "CMakeLists.txt"
cmake_minimum_required(VERSION 3.10)
project($name)

string(TOUPPER "\${PROJECT_NAME}" PROJECT_NAME_U)

set(CMAKE_CXX_FLAGS "-O3 -Wall -g \${CMAKE_CXX_FLAGS} -pthread")

if(NOT DEFINED ${name_upper}_VERSION)
  set(${name_upper}_VERSION_MAJOR 1)
  set(${name_upper}_VERSION_MINOR 0)
  set(${name_upper}_VERSION_PATCH 0)
  set(${name_upper}_VERSION \${${name_upper}_VERSION_MAJOR}.\${${name_upper}_VERSION_MINOR}.\${${name_upper}_VERSION_PATCH})
  set(CMAKE_INSTALL_PREFIX \${CMAKE_CURRENT_SOURCE_DIR}/install/\${PROJECT_NAME}-\${${name_upper}_VERSION})
endif()

include(FindPkgConfig)
include(cmake/global_definition.cmake)

include_directories(
  include
)

### add your cmake configuration here ###
#########################################

# generate and install CMakeconfig files
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  "\${PROJECT_NAME}ConfigVersion.cmake"
  VERSION \${${name_upper}_VERSION}
  COMPATIBILITY SameMajorVersion)

install(FILES \${CMAKE_CURRENT_BINARY_DIR}/\${PROJECT_NAME}ConfigVersion.cmake
  DESTINATION \${CMAKE_INSTALL_PREFIX}/cmake/\${PROJECT_NAME})

EOF

if [ "$type" == "lib" ]; then
  cat <<EOF >> "CMakeLists.txt"
configure_file(
  \${CMAKE_CURRENT_SOURCE_DIR}/cmake/\${PROJECT_NAME}Config.cmake.in
  \${CMAKE_CURRENT_SOURCE_DIR}/cmake/\${PROJECT_NAME}Config.cmake
)
install(FILES \${CMAKE_CURRENT_SOURCE_DIR}/cmake/\${PROJECT_NAME}Config.cmake
  DESTINATION \${CMAKE_INSTALL_PREFIX}/cmake/\${PROJECT_NAME})

EOF
fi

# create cbuild.sh
cat <<EOF > "cbuild.sh"

# colorful output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

rm -rf build &&
rm -rf install &&

echo -e "\${BLUE}Start working.\${NC}"

# set variable
echo -e "\${BLUE}Start setting variables.\${NC}"
PROJECT_NAME=$name
PROJECT_NAME_U=\$(echo "\$PROJECT_NAME" | tr '[:lower:]' '[:upper:]')
PROJECT_NAME_L=\$(echo "\$PROJECT_NAME" | tr '[:upper:]' '[:lower:]')

${name_upper}_VERSION_MAJOR=1
${name_upper}_VERSION_MINOR=0
${name_upper}_VERSION_PATCH=0
${name_upper}_VERSION=\${${name_upper}_VERSION_MAJOR}.\${${name_upper}_VERSION_MINOR}.\${${name_upper}_VERSION_PATCH}

EOF

if [ "$type" == "lib" ]; then
  cat <<EOF >> "cbuild.sh"
BUILD_TEST=FALSE

CMAKE_INSTALL_PREFIX=\$(realpath \$(dirname "\${BASH_SOURCE[0]}"))/install
echo -e "\${GREEN}Set variables completed.\${NC}"

# build
echo -e "\${BLUE}Start building.\${NC}"
mkdir -p build &&
cd build &&
cmake -D${name_upper}_VERSION=\${${name_upper}_VERSION} \\
      -DCMAKE_INSTALL_PREFIX=\$CMAKE_INSTALL_PREFIX \\
      -DBUILD_TEST=\$BUILD_TEST \\
      ..

if [ ! \$? -eq 0 ]; then
  echo -e "\${RED}Failed to build.\${NC}"
  exit
fi

make install

if [ ! \$? -eq 0 ]; then
  echo -e "\${RED}Failed to build.\${NC}"
  exit
fi

echo -e "\${GREEN}Build completed.\${NC}"

echo -e "\${GREEN}All tasks have been done.\${NC}"

EOF
elif [ "$type" == "app" ]; then
  cat <<EOF >> "cbuild.sh"
NEED_PACK=false

CMAKE_INSTALL_PREFIX=\$(pwd)/install/\$PROJECT_NAME-${name_upper}_VERSION
echo -e "\${GREEN}Set variables completed.\${NC}"

# build
echo -e "\${BLUE}Start building.\${NC}"
mkdir -p build &&
cd build &&
cmake -D{PROJECT_NAME_U}_VERSION=${name_upper}_VERSION \\
      -DCMAKE_INSTALL_PREFIX=\$CMAKE_INSTALL_PREFIX \\
      -DNEED_PACK=\$NEED_PACK \\
      .. &&
make install

if [ ! \$? -eq 0 ]; then
  echo -e "\${RED}Failed to build.\${NC}"
  exit
fi

echo -e "\${GREEN}Build completed.\${NC}"

# pack
if [ "\$#" -eq 0 ] || [ \$1 != "pack" ] || [ ! NEED_PACK ]; then
  echo -e "\${BLUE}Skip packing.\${NC}"
  echo -e "\${GREEN}All tasks have been done.\${NC}"
  exit
fi

echo -e "\${BLUE}Start packing.\${NC}"

mkdir -p ../install &&
cd ../install &&
tar -zcvf \$PROJECT_NAME-${name_upper}_VERSION.tar.gz \$PROJECT_NAME-${name_upper}_VERSION &&
cd \$PROJECT_NAME-${name_upper}_VERSION &&

dpkg-buildpackage -us -uc &&

cd .. &&

sudo dpkg --purge \$PROJECT_NAME &&

sudo dpkg -i \${PROJECT_NAME_L}_1.0.0_amd64.deb 

date "+%Y-%m-%d %H:%M"
echo -e "\${GREEN}All tasks have been done: \${NC}"

EOF
fi

chmod +x cbuild.sh