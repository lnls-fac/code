#ifndef _POS_H
#define _POS_H

// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

template <typename T = double>
class Pos {
public:
	T rx;
	T px;
	T ry;
	T py;
	T de;
	T dl;
	typedef T type;
	Pos(const T& rx_ = 0, const T& px_ = 0, const T& ry_ = 0, const T& py_ = 0, const T& de_ = 0, const T& dl_ = 0);
};


template <typename T>
Pos<T>::Pos(const T& rx_, const T& px_, const T& ry_, const T& py_, const T& de_, const T& dl_):
rx(rx_), px(px_),
ry(ry_), py(py_),
de(de_), dl(dl_)
{

}


#endif
