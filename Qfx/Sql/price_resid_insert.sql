INSERT INTO `price_resid` (
	`symbol`,
	`time_frames`,
	`samples`,
	`frequency`,
	`shift_time_left`,
	`shift_time_right`,
	`shift_time`,
	`value`
) VALUES (
	'{strSymbol}',
	'{strTimeFrames}',
	{nSamples},
	{nFrequency},
	'{strShiftTimeLeft}',
	'{strShiftTimeRight}',
	'{strShiftTime}',
	{fValue});