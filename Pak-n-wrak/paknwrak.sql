-- Drop changes
DROP TRIGGER IF EXISTS calc_total_trigger
    ON Huurovereenkomst;
DROP FUNCTION calc_total_func();
DROP FUNCTION calc_extra_func(curr_object_id integer);
ALTER TABLE huurovereenkomst
    DROP COLUMN IF EXISTS totaalprijs;

-- Add column
ALTER TABLE huurovereenkomst
ADD COLUMN totaalprijs decimal(5,2) DEFAULT 0;

-- Calculate value of an extra
CREATE FUNCTION calc_extra_func(curr_object_id integer)
RETURNS decimal(5,2) AS 
$$
    DECLARE
        total decimal(5,2) DEFAULT 0;
    BEGIN
        -- SELECT NEW.HuurobjectID INTO curr_object;
        LOOP
            EXIT WHEN curr_object_id IS NULL;

            SELECT (total + "PrijsPerDag"), "HuurobjectID_Benodigd"
            INTO total, curr_object_id
            FROM Huurobject
            WHERE Huurobject."ID" = curr_object_id;
        END LOOP;
    --   INSERT INTO logs (aktion, tabelle, benutzer_id) VALUES(TG_OP, 'dateien', NEW.benutzer_id);
    RETURN total;
    END;
$$
LANGUAGE 'plpgsql';



-- Update total price for a contract
CREATE FUNCTION calc_total_func()
RETURNS TRIGGER AS
$$
    BEGIN
        SELECT SUM(calc_extra_func(relevant_extra."HuurobjectID"))
        INTO NEW.totaalprijs
        FROM (
            SELECT extra."HuurobjectID"
            FROM extra
            WHERE extra."Factuurnummer" = NEW."Factuurnummer"
        ) relevant_extra;
        RETURN NEW;
    END;
$$
LANGUAGE 'plpgsql';


-- Add trigger
CREATE TRIGGER calc_total_trigger BEFORE INSERT OR UPDATE
ON Huurovereenkomst
FOR EACH ROW
EXECUTE PROCEDURE calc_total_func();


-- Update all values
-- The actual totaalprijs will be set by trigger
UPDATE Huurovereenkomst
SET totaalprijs = 0;

-- Get some values to confirm
SELECT 
    Huurovereenkomst."Factuurnummer",
    Huurovereenkomst.totaalprijs,
    Extra."HuurobjectID",
    Huurobject."PrijsPerDag",
    Huurobject."HuurobjectID_Benodigd"
FROM Huurovereenkomst
INNER JOIN Extra
ON (Extra."Factuurnummer" = Huurovereenkomst."Factuurnummer")
INNER JOIN Huurobject
ON (Extra."HuurobjectID" = Huurobject."ID");