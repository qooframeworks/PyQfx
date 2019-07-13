DELETE
FROM
    `price_trend` AS `T1`
WHERE
    `T1`.`symbol`           =   '{strSymbol}'           AND
    `T1`.`time_frames`      =   '{strTimeFrames}'       AND
    `T1`.`samples`          =   {nSamples}              AND
    `T1`.`frequency`        =   {nFrequency}            AND
    `T1`.`shift_time_left`  =   '{strShiftTimeLeft}'    AND
    `T1`.`shift_time_right` =   '{strShiftTimeRight}'   AND
    `T1`.`shift_time`       =   '{strShiftTime}';