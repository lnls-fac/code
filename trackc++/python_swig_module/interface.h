#ifndef INTERFACE_H
#define INTERFACE_H

#include <vector>
#include "accelerator.h"
#include "auxiliary.h"
#include "tracking.h"
#include "pos.h"

struct LinePassArgs {
    unsigned int element_offset;
    Plane::type lost_plane;
    bool trajectory;
};

struct RingPassArgs : public LinePassArgs {
    unsigned int nr_turns;
    unsigned int lost_turn;
};

Status::type track_linepass_wrapper (
        const Accelerator& accelerator,
        Pos<double>& orig_pos,
        std::vector< Pos<double> >& pos,
        LinePassArgs& args);

Status::type track_ringpass_wrapper (
        const Accelerator& accelerator,
        Pos<double> &orig_pos,
        std::vector< Pos<double> >& pos,
        RingPassArgs& args);

#endif // INTERFACE_H
