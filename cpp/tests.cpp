#include "core.hpp"
#include <cassert>
#include <cmath>
#include <stdexcept>
int main(){using namespace lord_sumi;auto v=predict({2,4,6},2,2);assert(v.size()==2);assert(std::abs(v[0]-5)<1e-10);assert(std::abs(v[1]-5.5)<1e-10);assert(std::abs(backtest_mae({2,4,6},2)-3)<1e-10);bool bad=false;try{predict({1,-1},2,1);}catch(const std::invalid_argument&){bad=true;}assert(bad);bad=false;try{predict({1},1,366);}catch(const std::invalid_argument&){bad=true;}assert(bad);}