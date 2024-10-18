-- Creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE finished INT DEFAULT 0;
	DECLARE current_user_id INT;

	-- Declare a cursor to iterate through all users
	DECLARE user_cursor CURSOR FOR SELECT id FROM users;

	-- Declare a handler to set finished to 1 when there are no more rows
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

	-- Open the cursor
	OPEN user_cursor;

	-- Loop through each user in the users table
	user_loop: LOOP
		-- Fetch the current user's ID
		FETCH user_cursor INTO current_user_id;

		-- If there are no more users, exit the loop
        	IF finished = 1 THEN
            		LEAVE user_loop;
        	END IF;

		-- Calculate the total weighted score and total weight for the current user
		UPDATE users u
		SET u.average_score = (
			SELECT IFNULL(SUM(c.score * p.weight) / SUM(p.weight), 0)
			FROM corrections c
			JOIN projects p ON c.project_id = p.id
			WHERE c.user_id = current_user_id
		)
		WHERE u.id = current_user_id;
	
	END LOOP;

	-- Close the cursor
	CLOSE user_cursor;
END $$

DELIMITER ;
