-- Drop changes
DROP TRIGGER IF EXISTS calc_total_trigger ON Extra;
DROP TRIGGER IF EXISTS calc_total_reduced_trigger ON Extra;
DROP FUNCTION IF EXISTS calc_total_func();
DROP FUNCTION IF EXISTS calc_total_reduced_func();
DROP FUNCTION IF EXISTS calc_extra_func(curr_object_id integer);
ALTER TABLE huurovereenkomst
    DROP COLUMN IF EXISTS totaalprijs;

DROP TRIGGER IF EXISTS check_available_trigger ON Extra;
DROP FUNCTION IF EXISTS check_available_func();

-- These values are later inserted as tests
DELETE FROM EXTRA 
WHERE "Factuurnummer" = 100203
AND "HuurobjectID" = 6;

DELETE FROM EXTRA 
WHERE "Factuurnummer" = 849763
AND "HuurobjectID" = 4;


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
        UPDATE Huurovereenkomst
        SET totaalprijs = calc_query.total
        FROM 
        (
            SELECT 
            SUM(calc_extra_func(relevant_extra."HuurobjectID") 
                * (new_overeenkomst."TotDatum"::date - new_overeenkomst."VanDatum"::date)) 
                as total
            FROM 
            (
                SELECT extra."HuurobjectID"
                FROM extra
                WHERE extra."Factuurnummer" = NEW."Factuurnummer"
            ) relevant_extra,
            (   
                SELECT * 
                FROM Huurovereenkomst
                WHERE "Factuurnummer" = NEW."Factuurnummer" 
            ) new_overeenkomst
        ) calc_query
        WHERE Huurovereenkomst."Factuurnummer" = NEW."Factuurnummer";
        RETURN NEW;
    END;
$$
LANGUAGE 'plpgsql';



-- Update total price for a contract
CREATE FUNCTION calc_total_reduced_func()
RETURNS TRIGGER AS
$$
    BEGIN
        UPDATE Huurovereenkomst
        SET totaalprijs = (Huurovereenkomst.totaalprijs - calc_query.total)
        FROM 
        (
            SELECT 
            SUM(calc_extra_func(relevant_extra."HuurobjectID") 
                * (updated_overeenkomst."TotDatum"::date - updated_overeenkomst."VanDatum"::date))
                as total
            FROM 
            (
                SELECT extra."HuurobjectID"
                FROM extra
                WHERE extra."Factuurnummer" = OLD."Factuurnummer"
            ) relevant_extra,
            (   
                SELECT * 
                FROM Huurovereenkomst
                WHERE "Factuurnummer" = OLD."Factuurnummer" 
            ) updated_overeenkomst
        ) calc_query
        WHERE Huurovereenkomst."Factuurnummer" = OLD."Factuurnummer";
        RETURN NEW;
    END;
$$
LANGUAGE 'plpgsql';



-- Add trigger
CREATE TRIGGER calc_total_trigger AFTER INSERT OR UPDATE
ON EXTRA
FOR EACH ROW
EXECUTE PROCEDURE calc_total_func();



-- Add trigger for deleted extras
CREATE TRIGGER calc_total_reduced_trigger AFTER DELETE
ON EXTRA
FOR EACH ROW
EXECUTE PROCEDURE calc_total_reduced_func();



-- Throw exception if new rental period is invalid
CREATE FUNCTION check_available_func()
RETURNS TRIGGER AS
$$
    DECLARE
        num_conflicts integer DEFAULT 0;
        new_start date;
        new_end date;
    BEGIN
        -- Don't check if nothing was changed
        if TG_OP = 'UPDATE'
        AND OLD."Factuurnummer" = NEW."Factuurnummer"
        AND OLD."HuurobjectID" = NEW."HuurobjectID" THEN
            RETURN NEW;
        END IF;

        SELECT "VanDatum", "TotDatum"
        INTO new_start, new_end
        FROM Huurovereenkomst
        WHERE "Factuurnummer" = NEW."Factuurnummer";

        SELECT COUNT(object_overeenkomsten."Factuurnummer")
        INTO num_conflicts
        FROM 
        (
            SELECT 
                h2."Factuurnummer", 
                h2."VanDatum", 
                h2."TotDatum"
            FROM Huurovereenkomst h2
            INNER JOIN Extra e2
            ON (e2."Factuurnummer" = h2."Factuurnummer")
            WHERE e2."HuurobjectID" = NEW."HuurobjectID"
        ) object_overeenkomsten
        WHERE (object_overeenkomsten."VanDatum", object_overeenkomsten."TotDatum")
              OVERLAPS
              (new_start, new_end);
        
        IF num_conflicts > 0 THEN
            RAISE EXCEPTION 'Object already reserved';
        END IF;
        RETURN NEW;
    END;
$$
LANGUAGE 'plpgsql';



-- Add trigger to check availability of each extra as it is added
CREATE TRIGGER check_available_trigger BEFORE INSERT OR UPDATE
ON Extra
FOR EACH ROW
EXECUTE PROCEDURE check_available_func();



-- Get the values before database value changes
SELECT 
    Huurovereenkomst."Factuurnummer",
    Huurovereenkomst.totaalprijs,
    Huurovereenkomst."VanDatum",
    Huurovereenkomst."TotDatum",
    (Huurovereenkomst."TotDatum"::date - Huurovereenkomst."VanDatum"::date) as duration,
    Extra."HuurobjectID",
    Huurobject."PrijsPerDag",
    Huurobject."HuurobjectID_Benodigd"
FROM Huurovereenkomst
INNER JOIN Extra
ON (Extra."Factuurnummer" = Huurovereenkomst."Factuurnummer")
INNER JOIN Huurobject
ON (Extra."HuurobjectID" = Huurobject."ID");



-- Update all extras
-- The huurovereenkomst totaalprijs will be set by trigger
UPDATE Extra e
SET    "Factuurnummer" = e."Factuurnummer";

-- Add legal value
INSERT INTO Extra VALUES(100203, 6);

-- Add illegal value
INSERT INTO Extra VALUES(849763, 4);



-- Get values after changes
SELECT 
    Huurovereenkomst."Factuurnummer",
    Huurovereenkomst.totaalprijs,
    Huurovereenkomst."VanDatum",
    Huurovereenkomst."TotDatum",
    (Huurovereenkomst."TotDatum"::date - Huurovereenkomst."VanDatum"::date) as duration,
    Extra."HuurobjectID",
    Huurobject."PrijsPerDag",
    Huurobject."HuurobjectID_Benodigd"
FROM Huurovereenkomst
INNER JOIN Extra
ON (Extra."Factuurnummer" = Huurovereenkomst."Factuurnummer")
INNER JOIN Huurobject
ON (Extra."HuurobjectID" = Huurobject."ID");