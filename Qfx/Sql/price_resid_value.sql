SELECT
    `T1`.`shift_time` AS `shift_time`,
    `T1`.`value` AS `value`
FROM
    `price_resid` AS `T1`
WHERE
    `T1`.`symbol`       =   '{strSymbol}'                       AND
    `T1`.`time_frames`  =   '{strTimeFrames}'                   AND
    `T1`.`samples`      =   {nSamples}                          AND
    `T1`.`frequency`    =   {nFrequency}                        AND
	'{strShiftTimeLeft}' {strOperator} `T1`.`shift_time_right`  AND
	`T1`.`shift_time_right` <= '{strShiftTimeRight}';