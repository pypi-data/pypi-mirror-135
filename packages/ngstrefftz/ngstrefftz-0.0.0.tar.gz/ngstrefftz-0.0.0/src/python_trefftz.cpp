#include <python_ngstd.hpp>
#include <solve.hpp>
#include <fem.hpp>
#include <comp.hpp>
#include "trefftzfespace.hpp"
#include "specialcoefficientfunction.hpp"
#include "twavetents.hpp"
#include "embtrefftz.hpp"

PYBIND11_MODULE(_trefftz,m) {
    py::module::import("ngsolve");
    m.attr("__name__") = "ngstrefftz";
    m.attr("__package__") = "ngstrefftz";

    ExportTrefftzFESpace(m);
    ExportSpecialCoefficientFunction(m);
    ExportTWaveTents(m);
    ExportEmbTrefftz(m);
}

