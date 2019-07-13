SELECT
    `T1`.`shift_time`,
    `T1`.`close`
FROM
    `price_history` AS `T1`
WHERE
    `T1`.`symbol`       = '{strSymbol}'                         AND
    `T1`.`time_frames`  = '{strTimeFrames}'                     AND
	'{strShiftTimeLeft}' {strOperator} `T1`.`shift_time`        AND
	`T1`.`shift_time`   <= '{strShiftTimeRight}';