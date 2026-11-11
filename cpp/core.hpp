#pragma once
#include <cmath>
#include <cstddef>
#include <stdexcept>
#include <vector>
namespace lord_sumi {
inline double moving_average(const std::vector<double>& v, std::size_t window) {
 if (!window || v.size()<window) throw std::invalid_argument("insufficient history or invalid window");
 double sum=0;
 for(std::size_t i=v.size()-window;i<v.size();++i) {if(!std::isfinite(v[i])||v[i]<0) throw std::invalid_argument("invalid demand");sum+=v[i];}
 if(!std::isfinite(sum)) throw std::overflow_error("sum overflow");
 return sum/static_cast<double>(window);
}
inline std::vector<double> predict(std::vector<double> history,std::size_t window,std::size_t horizon) {
 if(!horizon||horizon>365||!window||window>history.size()) throw std::invalid_argument("invalid horizon or window");
 for(double x:history) if(!std::isfinite(x)||x<0) throw std::invalid_argument("invalid history");
 std::vector<double> out;out.reserve(horizon);
 for(std::size_t i=0;i<horizon;++i){double p=moving_average(history,window);out.push_back(p);history.push_back(p);}
 return out;
}
inline double backtest_mae(const std::vector<double>& history,std::size_t window){
 if(!window||history.size()<=window)throw std::invalid_argument("insufficient history");
 for(double x:history)if(!std::isfinite(x)||x<0)throw std::invalid_argument("invalid history");
 double total=0;for(std::size_t i=window;i<history.size();++i){std::vector<double> past(history.begin(),history.begin()+i);total+=std::abs(history[i]-moving_average(past,window));}
 return total/(history.size()-window);
}
}