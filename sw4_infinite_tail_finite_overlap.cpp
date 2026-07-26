#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using i64 = std::int64_t;
using i128 = __int128_t;
using State = std::vector<int>;
using Group = std::vector<State>;
using Interval = std::pair<i64, i64>;

static i128 choose3(i64 n) {
    if (n < 3) return 0;
    return (i128)n * (n - 1) * (n - 2) / 6;
}

static i128 choose4(i64 n) {
    if (n < 4) return 0;
    return (i128)n * (n - 1) * (n - 2) * (n - 3) / 24;
}

static i64 star_value(int n) {
    return (i64)((i128)(n - 1) * choose3(n - 1));
}

static i64 increment(int n, int a) {
    return (i64)(choose4(n - 1) - choose4(a) - choose4(n - a));
}

static i64 central_increment(int h, int x) {
    return increment(2 * h, h + x);
}

static i64 state_value(int h, const State& state) {
    i128 total = 0;
    for (int x : state) total += central_increment(h, x);
    assert(total >= 0 && total <= std::numeric_limits<i64>::max());
    return (i64)total;
}

static i64 square_sum(const State& s) {
    i64 z = 0;
    for (i64 x : s) z += x * x;
    return z;
}

static i64 fourth_sum(const State& s) {
    i128 z = 0;
    for (i64 x : s) z += (i128)x * x * x * x;
    assert(z <= std::numeric_limits<i64>::max());
    return (i64)z;
}

static std::vector<Interval> add_optional_weight(
    const std::vector<Interval>& input,
    i64 weight
) {
    // Exact merge of S and S+weight, where S is represented by sorted,
    // pairwise-disjoint maximal integer intervals.
    const std::size_t n = input.size();
    std::size_t i = 0, j = 0;
    std::vector<Interval> output;
    output.reserve(2 * n);

    while (i < n || j < n) {
        Interval current;
        if (j >= n || (i < n && input[i].first <= input[j].first + weight)) {
            current = input[i++];
        } else {
            current = {input[j].first + weight, input[j].second + weight};
            ++j;
        }

        if (output.empty() || current.first > output.back().second + 1) {
            output.push_back(current);
        } else if (current.second > output.back().second) {
            output.back().second = current.second;
        }
    }
    return output;
}

static Group three_state_unit_base() {
    return {
        {0, 2, 2, 3, 6, 6, 10, 10, 12, 12},
        {1, 1, 4, 4, 6, 7, 8, 9, 12, 13},
        {1, 1, 4, 5, 5, 7, 7, 11, 11, 13}
    };
}

static Group independent_unit_pair() {
    return {
        {16, 22, 24, 27, 30, 32, 36},
        {17, 20, 25, 26, 31, 33, 35}
    };
}

static std::vector<Group> seed51_groups() {
    std::vector<Group> groups = {three_state_unit_base(), independent_unit_pair()};
    groups.push_back({{23, 28, 32, 49}, {18, 25, 42, 45}}); // 4
    groups.push_back({{16, 24, 45, 51}, {8, 28, 47, 49}});  // 8
    groups.push_back({{20, 29, 46, 50}, {14, 36, 42, 51}}); // 16
    groups.push_back({{9, 39, 39, 46}, {23, 29, 37, 50}});  // 32
    return groups;
}

static std::vector<Group> seed65_groups() {
    std::vector<Group> groups = {three_state_unit_base(), independent_unit_pair()};
    groups.push_back({{23, 28, 32, 49}, {18, 25, 42, 45}}); // 4
    groups.push_back({{21, 24, 45, 51}, {19, 27, 43, 52}}); // 8
    groups.push_back({{14, 38, 55, 55}, {3, 43, 54, 54}});  // 16
    groups.push_back({{9, 39, 39, 46}, {23, 29, 37, 50}});  // 32
    groups.push_back({{17, 28, 44, 59}, {15, 36, 37, 60}}); // 64
    groups.push_back({{18, 35, 48, 48}, {26, 29, 44, 52}}); // 128
    groups.push_back({{20, 40, 58, 65}, {16, 42, 60, 63}}); // 256
    groups.push_back({{57, 57, 63, 64}, {56, 59, 61, 65}}); // 512
    groups.push_back({{14, 34, 41, 53}, {15, 30, 46, 51}}); // 1024
    return groups;
}

static std::vector<Group> seed100_groups() {
    std::vector<Group> groups = {three_state_unit_base(), independent_unit_pair()};
    groups.push_back({{72,78,85,90}, {73,76,88,88}}); // 4
    groups.push_back({{8,58,71,73}, {45,46,51,84}}); // 8
    groups.push_back({{77,83,90,95}, {78,81,93,93}}); // 16
    groups.push_back({{81,87,94,99}, {82,85,97,97}}); // 32
    groups.push_back({{22,43,64,71}, {25,48,54,75}}); // 64
    groups.push_back({{15,28,39,51}, {23,23,37,52}}); // 128
    groups.push_back({{9,24,64,87}, {29,40,40,91}}); // 256
    groups.push_back({{14,14,29,35}, {18,18,21,37}}); // 512
    groups.push_back({{28,31,86,92}, {30,33,80,96}}); // 1024
    groups.push_back({{16,60,66,66}, {16,62,62,68}}); // 2048
    groups.push_back({{55,61,67,70}, {57,58,69,69}}); // 4096
    groups.push_back({{26,41,53,65}, {27,38,57,63}}); // 8192
    groups.push_back({{3,60,67,75}, {19,53,68,77}}); // 16384
    groups.push_back({{13,20,43,47}, {15,21,44,45}}); // 32768
    groups.push_back({{38,50,56,70}, {42,46,54,72}}); // 65536
    groups.push_back({{32,52,76,100}, {36,44,84,96}}); // 131072
    return groups;
}

struct Construction {
    i64 baseline;
    i64 seed_width;
    std::vector<i64> independent_weights;
    std::vector<int> demand;
};

static std::vector<int> state_counter(const State& s, int h) {
    std::vector<int> c(h - 1, 0);
    for (int x : s) {
        assert(0 <= x && x <= h - 2);
        ++c[x];
    }
    return c;
}

static Construction reserve_groups(
    int h,
    const std::vector<Group>& groups,
    i64 seed_width
) {
    Construction out;
    out.baseline = star_value(2 * h);
    out.seed_width = seed_width;
    out.demand.assign(h - 1, 0);

    for (const Group& group : groups) {
        assert(!group.empty());
        const std::size_t cardinality = group.front().size();
        const i64 sq = square_sum(group.front());
        std::vector<i64> values;
        std::vector<std::vector<int>> counters;

        for (const State& state : group) {
            assert(state.size() == cardinality);
            assert(square_sum(state) == sq);
            values.push_back(state_value(h, state));
            counters.push_back(state_counter(state, h));
        }

        out.baseline += *std::min_element(values.begin(), values.end());
        for (int x = 0; x <= h - 2; ++x) {
            int need = 0;
            for (const auto& counter : counters) need = std::max(need, counter[x]);
            out.demand[x] += need;
        }
    }

    for (int x = 0; x <= h - 2; ++x) {
        const int capacity = (x == 0 ? 1 : 2);
        assert(out.demand[x] <= capacity);
    }
    return out;
}

static std::pair<State, State> thue_morse_states(int R, int q, int r) {
    State even, odd;
    for (int j = 0; j < 8; ++j) {
        const int x = R + r + j * q;
        if (__builtin_popcount((unsigned)j) % 2 == 0) even.push_back(x);
        else odd.push_back(x);
    }
    return {even, odd};
}

static void reserve_annulus(Construction& c, int h, int R, int q) {
    for (int r = 0; r < q; ++r) {
        auto [a, b] = thue_morse_states(R, q, r);
        const i64 va = state_value(h, a);
        const i64 vb = state_value(h, b);
        const i64 d = std::llabs(va - vb);
        const i64 formula = (i64)8 * q * q * q * (2LL * (R + r) + 7LL * q);
        assert(d == formula);
        c.baseline += std::min(va, vb);
        c.independent_weights.push_back(d);

        std::set<int> support;
        support.insert(a.begin(), a.end());
        support.insert(b.begin(), b.end());
        for (int x : support) {
            assert(0 <= x && x <= h - 2);
            ++c.demand[x];
            const int capacity = (x == 0 ? 1 : 2);
            assert(c.demand[x] <= capacity);
        }
    }
}

static std::vector<Interval> certify_order(
    int h,
    const std::vector<Group>& groups,
    i64 seed_width,
    const std::vector<std::pair<int,int>>& annuli,
    std::size_t& maximum_interval_count
) {
    Construction c = reserve_groups(h, groups, seed_width);
    for (auto [R, q] : annuli) reserve_annulus(c, h, R, q);

    for (int x = 0; x <= h - 2; ++x) {
        const int capacity = (x == 0 ? 1 : 2);
        for (int k = c.demand[x]; k < capacity; ++k) {
            c.independent_weights.push_back(central_increment(h, x));
        }
    }

    std::sort(c.independent_weights.begin(), c.independent_weights.end());
    std::vector<Interval> intervals = {{0, seed_width}};
    maximum_interval_count = intervals.size();
    for (i64 weight : c.independent_weights) {
        intervals = add_optional_weight(intervals, weight);
        maximum_interval_count = std::max(maximum_interval_count, intervals.size());
    }

    for (Interval& interval : intervals) {
        interval.first += c.baseline;
        interval.second += c.baseline;
    }
    return intervals;
}

static Interval longest_interval(const std::vector<Interval>& intervals) {
    return *std::max_element(
        intervals.begin(), intervals.end(),
        [](const Interval& a, const Interval& b) {
            return a.second - a.first < b.second - b.first;
        }
    );
}

static void verify_group_digits(const std::vector<Group>& groups, i64 expected_width) {
    // Equal cardinality and equal square sum make every difference independent of h.
    // delta_h(x)=A_h+B_h*x^2-x^4/12.
    std::vector<i64> digit_maxima;
    for (std::size_t i = 0; i < groups.size(); ++i) {
        const Group& group = groups[i];
        const std::size_t cardinality = group.front().size();
        const i64 sq = square_sum(group.front());
        std::vector<i64> q4;
        for (const State& state : group) {
            assert(state.size() == cardinality);
            assert(square_sum(state) == sq);
            q4.push_back(fourth_sum(state));
        }
        std::sort(q4.begin(), q4.end());
        std::vector<i64> normalized;
        for (i64 z : q4) normalized.push_back((q4.back() - z) / 12);
        std::sort(normalized.begin(), normalized.end());
        normalized.erase(std::unique(normalized.begin(), normalized.end()), normalized.end());

        if (i == 0) {
            assert((normalized == std::vector<i64>{0,1,2}));
        } else {
            assert(normalized.size() == 2 && normalized[0] == 0);
            digit_maxima.push_back(normalized[1]);
        }
    }
    std::sort(digit_maxima.begin(), digit_maxima.end());
    i64 width = 2; // three-state group realizes 0,1,2.
    for (i64 d : digit_maxima) {
        assert(d <= width + 1);
        width += d;
    }
    assert(width == expected_width);
}

int main() {
    constexpr i64 OLD_COVERAGE_END = 554860689583;
    constexpr i64 UNIVERSAL_L_365 = 1596122112921;

    const auto seed51 = seed51_groups();
    const auto seed65 = seed65_groups();
    const auto seed100 = seed100_groups();
    verify_group_digits(seed51, 63);
    verify_group_digits(seed65, 2047);
    verify_group_digits(seed100, 262143);

    std::ofstream table("sw4_infinite_tail_finite_overlap.csv");
    assert(table);
    table << "family,h,n,L,U,final_interval_count,max_interval_count\n";

    i64 covered_end = OLD_COVERAGE_END;
    i64 first_new_start = -1;

    auto run_chain = [&](const std::string& name, int h0, int h1,
                         const std::vector<Group>& groups, i64 seed_width,
                         const std::vector<std::pair<int,int>>& annuli) {
        for (int h = h0; h <= h1; ++h) {
            std::size_t max_count = 0;
            const auto intervals = certify_order(h, groups, seed_width, annuli, max_count);
            const Interval best = longest_interval(intervals);
            if (first_new_start < 0) first_new_start = best.first;
            assert(best.first <= covered_end + 1);
            covered_end = std::max(covered_end, best.second);
            table << name << ',' << h << ',' << 2*h << ','
                  << best.first << ',' << best.second << ','
                  << intervals.size() << ',' << max_count << '\n';
            std::cout << name << " h=" << h << " n=" << 2*h
                      << " [" << best.first << ',' << best.second << "]"
                      << " intervals=" << intervals.size()
                      << " max_intervals=" << max_count << '\n';
        }
    };

    // Exact finite junction from the completed bridge to the universal family.



    // The annuli occupy 101..140 and 141..204.
    run_chain("seed100_TM", 253, 365, seed100, 262143, {{101,5},{141,8}});

    assert(first_new_start == 272308250181);
    assert(covered_end == 3868972697957);
    assert(UNIVERSAL_L_365 <= covered_end + 1);

    table << "SUMMARY,,,," << covered_end << ",,\n";
    std::cout << "PASS\n";
    std::cout << "bridge_start=" << first_new_start << '\n';
    std::cout << "bridge_end=" << covered_end << '\n';
    std::cout << "old_coverage_end=" << OLD_COVERAGE_END << '\n';
    std::cout << "universal_L_365=" << UNIVERSAL_L_365 << '\n';
    std::cout << "finite_chain=253..365\n";
    return 0;
}
