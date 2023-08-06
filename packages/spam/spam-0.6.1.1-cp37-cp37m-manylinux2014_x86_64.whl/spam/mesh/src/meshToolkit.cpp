#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <math.h>
#include <cmath>
#include <string.h>
#include <random>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
//#include <tiffio.h>
#include <algorithm>

#include "crpacking.hpp"
#include "projmorpho.hpp"
#include "connectivityMatrix.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(meshToolkit, m) {
  py::class_<crpacking>(m, "crpacking")
  .def(py::init<std::vector<double>,
    std::vector<double>,
    std::vector<double>,
    std::vector<unsigned int>,
    unsigned int,
    std::string,
    std::string,
    std::string>())
    .def("createSpheres", &crpacking::create_spheres, "create spheres")
    .def("packSpheres", &crpacking::pack_spheres, "pack spheres", py::arg("do_write_objects_vtk") = false)
    .def("convertToField", &crpacking::convert_to_field, "convert to field", py::arg("do_print_progress") = true)
    .def("getObjects", &crpacking::get_objects, "get objects")
    .def("setObjects", &crpacking::set_objects, "set objects")
    .def("writeField", &crpacking::write_field, "write field")
    .def("writeFieldVTK", &crpacking::write_field_vtk, "write field in vtk")
    .def("getField", &crpacking::get_field, "get field");

    py::class_<projmorpho>(m, "projmorpho")
    .def(py::init<const std::string,
      const std::vector<double>>())
      .def("setMesh", &projmorpho::set_mesh_vectors, "set mesh vectors")
      .def("debug", &projmorpho::debug, "debug")
      .def("setFieldFromFile", &projmorpho::set_field_from_file, "set field from file")
      .def("setField", &projmorpho::set_field_vectors, "set field vectors")
      .def("interpolateField", &projmorpho::interpolate_field, "interpolate field")
      .def("setMaterials", &projmorpho::set_materials, "set materials")
      .def("getConnectivity", &projmorpho::get_mesh_connectivity, "get connectivity")
      .def("getMaterials", &projmorpho::get_materials, "get materials")
      .def("writeMeshProjection", &projmorpho::write_mesh_projection, "write mesh projection")
      .def("writeInterfacesVTK", &projmorpho::write_interfaces_vtk, "write mesh interfaces")
      .def("writeMeshProjectionVTK", &projmorpho::write_mesh_projection_vtk, "write mesh projection vtk");

    m.def("countTetrahedraCGAL", &countTetrahedraCGAL, "countTetrahedraCGAL");
    m.def("triangulateCGAL", &triangulateCGAL, "triangulateCGAL");
    }
