SELECT
	`T1`.`symbol`,
    `T1`.`time_frames`,
    MIN(`T1`.`shift_time`) AS `shift_time_first`,
    MAX(`T1`.`shift_time`) AS `shift_time_last`,
    COUNT(*) AS `bars`
FROM
	`price_history` AS `T1`
GROUP BY
	`T1`.`symbol`,
    `T1`.`time_frames`;