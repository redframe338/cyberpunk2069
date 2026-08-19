-- Lightweight cyberpunk strategic-map palette.
-- Only changes existing colour calculations; no new effects or render passes.
NGraphics = {
	COUNTRY_COLOR_HUE_MODIFIER = 0.0,
	-- Muted, near-black political colours inspired by printed dystopian maps.
	-- Countries remain distinguishable, but bright vanilla colours are suppressed.
	COUNTRY_COLOR_SATURATION_MODIFIER = 0.48,
	COUNTRY_COLOR_BRIGHTNESS_MODIFIER = 0.42,

	-- Electric cyan state selection.
	BORDER_COLOR_SELECTION_STATE_R = 0.05,
	BORDER_COLOR_SELECTION_STATE_G = 0.90,
	BORDER_COLOR_SELECTION_STATE_B = 1.00,
	BORDER_COLOR_SELECTION_STATE_A = 1.00,

	-- Magenta supply-area selection.
	BORDER_COLOR_SELECTION_SUPPLY_AREA_R = 0.90,
	BORDER_COLOR_SELECTION_SUPPLY_AREA_G = 0.10,
	BORDER_COLOR_SELECTION_SUPPLY_AREA_B = 0.75,
	BORDER_COLOR_SELECTION_SUPPLY_AREA_A = 1.00,

	-- Amber province selection remains easy to distinguish from cyan borders.
	BORDER_COLOR_SELECTION_PROVINCE_R = 1.00,
	BORDER_COLOR_SELECTION_PROVINCE_G = 0.62,
	BORDER_COLOR_SELECTION_PROVINCE_B = 0.08,
	BORDER_COLOR_SELECTION_PROVINCE_A = 1.00,

	SUPPLY_COUNTRY_BORDER_PLAYER_COLOR = { 0.05, 0.95, 0.78, 1.0 },
	SUPPLY_COUNTRY_BORDER_FRIEND_COLOR = { 0.05, 0.62, 1.00, 1.0 },
	SUPPLY_COUNTRY_BORDER_ACCESS_COLOR = { 0.72, 0.22, 1.00, 1.0 },
}
