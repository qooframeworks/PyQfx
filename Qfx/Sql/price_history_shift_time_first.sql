SELECT
	MIN(`T1`.`shift_time`)	AS `shift_time`
FROM
	`price_history`	AS `T1`
WHERE
	`T1`.`symbol`		= '{strSymbol}'			AND
	`T1`.`time_frames`	= '{strTimeFrames}';