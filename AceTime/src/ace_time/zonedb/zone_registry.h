// This file was generated by the following script:
//
//   $ /home/brian/src/AceTimeTools/src/acetimetools/tzcompiler.py
//     --input_dir /home/brian/dev/tz
//     --output_dir /home/brian/src/AceTime/src/ace_time/zonedb
//     --tz_version 2021e
//     --action zonedb
//     --language arduino
//     --scope basic
//     --start_year 2000
//     --until_year 2050
//
// using the TZ Database files
//
//   africa
//   antarctica
//   asia
//   australasia
//   backward
//   etcetera
//   europe
//   northamerica
//   southamerica
//
// from https://github.com/eggert/tz/releases/tag/2021e
//
// DO NOT EDIT

#ifndef ACE_TIME_ZONEDB_ZONE_REGISTRY_H
#define ACE_TIME_ZONEDB_ZONE_REGISTRY_H

#include <ace_time/internal/ZoneInfo.h>
#include <ace_time/internal/LinkEntry.h>

namespace ace_time {
namespace zonedb {

// Zones
const uint16_t kZoneRegistrySize = 258;
extern const basic::ZoneInfo* const kZoneRegistry[258];

// Zones and Links
const uint16_t kZoneAndLinkRegistrySize = 451;
extern const basic::ZoneInfo* const kZoneAndLinkRegistry[451];

// Link Entries
const uint16_t kLinkRegistrySize = 193;
extern const basic::LinkEntry kLinkRegistry[193];

}
}
#endif
