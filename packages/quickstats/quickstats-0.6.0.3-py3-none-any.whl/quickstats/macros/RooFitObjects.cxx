#include "map"
#include "string"
#include "RooDataSet.h"
#include "RooAbsPdf.h"
#ifdef __CINT__ 
#pragma link C++ nestedclasses;
#pragma link C++ nestedtypedefs;
#pragma link C++ class std::map<std::string, RooDataSet*>+;
#pragma link C++ class std::map<std::string, RooDataSet*>::*;
#pragma link C++ class std::pair<std::map<string,RooDataSet*>::iterator, bool>+;
#pragma link C++ class std::pair<std::map<string,RooDataSet*>::iterator, bool>::*+;
#pragma link C++ class std::pair<std::string, RooDataSet*>+;
#pragma link C++ class std::pair<std::string, RooDataSet*>::*+;
#pragma link C++ class std::map<std::string, RooAbsPdf*>+;
#pragma link C++ class std::map<std::string, RooAbsPdf*>::*;
#pragma link C++ class std::pair<std::map<string,RooAbsPdf*>::iterator, bool>+;
#pragma link C++ class std::pair<std::map<string,RooAbsPdf*>::iterator, bool>::*+;
#pragma link C++ class std::pair<std::string, RooAbsPdf*>+;
#pragma link C++ class std::pair<std::string, RooAbsPdf*>::*+;
#endif
