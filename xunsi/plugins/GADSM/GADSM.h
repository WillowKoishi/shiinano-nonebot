#ifndef GADSM_H
#define GADSM_H

#include <array>

class GADSM_Result;

class GADSM
{
public:
	GADSM(const double MJD_0_ref, const double MJD_f_ref, const double C3, const std::array<int, 3> &sequence);
	~GADSM() = default;

	bool func(const double *x, double *F, GADSM_Result *result);

private:
	const double MJD_0_ref;
	const double MJD_f_ref;
	const double C3;
	const std::array<int, 3> sequence;

	friend GADSM_Result;
};

#endif // !GADSM_H
