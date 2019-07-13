SELECT
    COUNT(*)
FROM
    `price_history` AS `T1`
WHERE
    `T1`.`symbol`       = '{strSymbol}'             AND
    `T1`.`time_frames`  = '{strTimeFrames}'         AND
	'{strShiftTimeLeft}' <= `T1`.`shift_time`       AND
	`T1`.`shift_time`   <= '{strShiftTimeRight}';