DELETE
FROM
    `price_seasonal` AS `T1`
WHERE
    `T1`.`symbol`           =   '{strSymbol}'           AND
    `T1`.`time_frames`      =   '{strTimeFrames}'       AND
    `T1`.`samples`          =   {nSamples}              AND
    `T1`.`frequency`        =   {nFrequency};