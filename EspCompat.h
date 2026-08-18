#ifndef espcompat_h
#define espcompat_h
#include <ETH.h>
#if defined __has_include && __has_include(<esp_chip_info.h>)
#include <esp_chip_info.h>
#endif

/* Arduino ESP32 core 3.x (IDF 5.x) only declares the RMII ethernet symbols for targets
   that actually have an EMAC, which means plain ESP32.  Core 2.x declared them for every
   target and the settings structures below are shared by all builds, so fill in the gaps
   to keep them compiling on the S2/S3/C3 variants. */
#if ESP_ARDUINO_VERSION_MAJOR >= 3 && !CONFIG_ETH_USE_ESP32_EMAC
typedef enum {
  ETH_CLOCK_GPIO0_IN,
  ETH_CLOCK_GPIO0_OUT,
  ETH_CLOCK_GPIO16_OUT,
  ETH_CLOCK_GPIO17_OUT
} eth_clock_mode_t;
#define ETH_PHY_LAN8720 ETH_PHY_MAX
#endif

/* Defaulted unconditionally by core 2.x; in 3.x these only arrive from pins_arduino.h
   when a board declares an ethernet PHY.  Values match the core 2.x defaults. */
#ifndef ETH_PHY_ADDR
#define ETH_PHY_ADDR 0
#endif
#ifndef ETH_PHY_POWER
#define ETH_PHY_POWER -1
#endif
#ifndef ETH_PHY_MDC
#define ETH_PHY_MDC 23
#endif
#ifndef ETH_PHY_MDIO
#define ETH_PHY_MDIO 18
#endif
#endif
