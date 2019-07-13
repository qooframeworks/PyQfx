UPDATE `price_seasonal` SET
	`value` = {fValue}
WHERE
	`symbol`		    =   '{strSymbol}'           AND
	`time_frames`	    =   '{strTimeFrames}'       AND
    `samples`           =   {nSamples}              AND
	`frequency`         =   {nFrequency}            AND
	`shift_time_left`	=   '{strShiftTimeLeft}'    AND
	`shift_time_right`	=   '{strShiftTimeRight}'   AND
	`shift_time`        =   '{strShiftTime}';