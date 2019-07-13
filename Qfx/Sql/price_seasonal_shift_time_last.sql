SELECT
	`T1`.`shift_time_left`,
	`T1`.`shift_time_right`,
	`T1`.`shift_time`
FROM
	`price_seasonal`	AS `T1`
WHERE
	`T1`.`symbol`		=   '{strSymbol}'		AND
	`T1`.`time_frames`	=   '{strTimeFrames}'   AND
    `T1`.`samples`      =   {nSamples}          AND
	`T1`.`frequency`    =   {nFrequency}
ORDER BY
	`T1`.`shift_time` DESC
LIMIT 1;