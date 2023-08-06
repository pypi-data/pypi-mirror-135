#################################### Documentation ####################################
# -- USAGE --
#
# FIND_PACKAGE(carma CONFIG)
#     Creates the carma::carma and carma::headers targets
#
# FIND_PACKAGE(carma CONFIG COMPONENTS carma)
#     Creates only the carma::carma target
#
# FIND_PACKAGE(carma CONFIG COMPONENTS headers)
#     Creates only the carma::headers target
#
# The `REQUIRED` keyword is passed along to the dependencies of carma
#
# -- VARIABLES --
# This script sets:
# carma_INCLUDE_DIR -- include directory for carma
# carma_INCLUDE_DIRS -- include directory for carma and it's dependencies
# carma_LIBRARY -- empty
#
# -- TARGETS --
#
# carma::carma 
#     Target as produced by the cmake without installing.
#     Linked to: Pybind11, Armadillo, Python and Numpy
#     Pre-compiles cnalloc.h to prevent the include order restriction with armadillo
#
# carma::headers
#     Header only target, not linked to any dependency and does not include the
#     pre-compiled header.
#     NOTE when using this target carma must be included before armadillo
#
#######################################################################################


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was carmaConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

# Compute the installation prefix relative to this file.
GET_FILENAME_COMPONENT(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_FILE}" PATH)
GET_FILENAME_COMPONENT(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
GET_FILENAME_COMPONENT(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
GET_FILENAME_COMPONENT(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
IF(_IMPORT_PREFIX STREQUAL "/")
  SET(_IMPORT_PREFIX "")
ENDIF()

SET(_SUPPORTED_COMPONENTS "carma" "headers")

SET(carma_INCLUDE_DIR "${_IMPORT_PREFIX}/include/carma")
SET(carma_INCLUDE_DIRS "${_IMPORT_PREFIX}/include/carma")
set(carma_LIBRARY "")

FOREACH(_comp ${carma_FIND_COMPONENTS})
    IF (_comp STREQUAL "carma")
        INCLUDE("${CMAKE_CURRENT_LIST_DIR}/carmaDependencyTargets.cmake")
        INCLUDE("${CMAKE_CURRENT_LIST_DIR}/carmaCarmaTargets.cmake")
        SET(carma_carma_FOUND TRUE)
    ELSEIF (_comp STREQUAL "headers")
        INCLUDE("${CMAKE_CURRENT_LIST_DIR}/carmaHeaderTargets.cmake")
        SET(carma_headers_FOUND TRUE)
    ELSE ()
        SET(carma_NOT_FOUND_MESSAGE "Unsupported component: ${_comp}")
    ENDIF()
ENDFOREACH()
IF (NOT carma_carma_FOUND OR carma_headers_FOUND)
    INCLUDE("${CMAKE_CURRENT_LIST_DIR}/carmaDependencyTargets.cmake")
    INCLUDE("${CMAKE_CURRENT_LIST_DIR}/carmaCarmaTargets.cmake")
    INCLUDE("${CMAKE_CURRENT_LIST_DIR}/carmaHeaderTargets.cmake")
ENDIF ()

# add pre-compiled header such that import order doesn't matter
IF (TARGET carma::carma)
    TARGET_PRECOMPILE_HEADERS(carma::carma
        INTERFACE
            "${carma_INCLUDE_DIR}/carma_bits/cnalloc.h"
    )
ENDIF()
IF (TARGET carma::carma_headers)
    ADD_LIBRARY(carma::headers ALIAS carma::carma_headers)
ENDIF ()

check_required_components("carma")

IF (NOT carma_FIND_QUIETLY)
  message(
    STATUS
      "Found carma: ${carma_INCLUDE_DIR} (found version \"${carma_VERSION}\")"
  )
ENDIF()

# clean up
SET(_IMPORT_PREFIX)
SET(_SUPPORTED_COMPONENTS)
