
#include "interface.h"


Status::type track_linepass_wrapper(
        const Accelerator &accelerator,
        Pos<double> &orig_pos,
        std::vector< Pos<double> >& pos,
        LinePassArgs& args) {
    return track_linepass(accelerator,
                          orig_pos,
                          pos,
                          args.element_offset,
                          args.lost_plane,
                          args.trajectory);
}

Status::type track_ringpass_wrapper (
        const Accelerator& accelerator,
        Pos<double> &orig_pos,
        std::vector< Pos<double> >& pos,
        RingPassArgs& args) {
    return track_ringpass(accelerator,
                          orig_pos,
                          pos,
                          args.nr_turns,
                          args.lost_turn,
                          args.element_offset,
                          args.lost_plane,
                          args.trajectory);
}

Status::type track_findm66_wrapper (
        const Accelerator& accelerator,
        const std::vector<Pos<double> >& closed_orbit,
        std::vector<double*>& m66) {
    m66.clear();
    int n = accelerator.lattice.size();
    for (int i=0; i<n; ++i)
        m66.push_back(new double[36]);

    return track_findm66(accelerator, closed_orbit, m66);
}
