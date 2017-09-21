-- Drop changes
DROP TRIGGER IF EXISTS calc_total_trigger ON Extra;
DROP FUNCTION IF EXISTS calc_extra_total_func(factuur_nr INTEGER);
DROP FUNCTION IF EXISTS calc_car_total_func(factuur_nr INTEGER);
DROP FUNCTION IF EXISTS calc_total_func();
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



CREATE FUNCTION calc_car_total_func(factuur_nr INTEGER)
RETURNS DECIMAL(5,2) AS
$$
    DECLARE
        total decimal(5,2) DEFAULT 0;
    BEGIN
        -- SELECT SUM(
        --     Voertuigtype."PrijsPerDag" 
        --     * (Huurovereenkomst."TotDatum"::date - Huurovereenkomst."VanDatum"::date))
        -- INTO total
        -- FROM Huurovereenkomst
        -- INNER JOIN Voertuig
        -- ON Huurovereenkomst."VoertuigID" = Voertuig."ID"
        -- INNER JOIN Voertuigtype
        -- ON Voertuig."VoertuigtypeID" = Voertuigtype."ID"
        -- WHERE Huurovereenkomst."Factuurnummer" = factuur_nr;

        RETURN 0;
    END;
$$
LANGUAGE 'plpgsql';



CREATE FUNCTION calc_extra_total_func(factuur_nr INTEGER)
RETURNS decimal(5,2) AS
$$
    DECLARE
        total decimal(5,2) DEFAULT 0;
    BEGIN
        SELECT 
        SUM(calc_extra_func(relevant_extra."HuurobjectID") 
            * (new_overeenkomst."TotDatum"::date - new_overeenkomst."VanDatum"::date)) 
        INTO total
        FROM 
        (
            SELECT extra."HuurobjectID"
            FROM extra
            WHERE extra."Factuurnummer" = factuur_nr
        ) relevant_extra,
        (   
            SELECT * 
            FROM Huurovereenkomst
            WHERE "Factuurnummer" = factuur_nr
        ) new_overeenkomst;

        RETURN total;
    END;
$$
LANGUAGE 'plpgsql';


-- Update total price for a contract
CREATE FUNCTION calc_total_func()
RETURNS TRIGGER AS
$$
    DECLARE
        car_prijs decimal(5,2) DEFAULT 0;
        extra_prijs decimal(5,2) DEFAULT 0;
    BEGIN
        IF TG_OP = 'UPDATE'
        OR TG_OP = 'INSERT'
        THEN
            -- car_prijs = calc_extra_total_func(NEW."Factuurnummer");

            UPDATE Huurovereenkomst
            SET totaalprijs = (
                calc_extra_total_func(NEW."Factuurnummer") 
                + calc_car_total_func(NEW."Factuurnummer"))
            WHERE "Factuurnummer" = NEW."Factuurnummer";
        ELSEIF TG_OP = 'DELETE'
        THEN 
            UPDATE Huurovereenkomst
            SET totaalprijs = (
                calc_extra_total_func(OLD."Factuurnummer") 
                + calc_car_total_func(OLD."Factuurnummer"))
            WHERE "Factuurnummer" = OLD."Factuurnummer";
        END IF;

        -- raise notice 'Value: %', deletedContactId;
        
        RETURN NEW;
    END;
$$
LANGUAGE 'plpgsql';



-- Add trigger
CREATE TRIGGER calc_total_trigger AFTER INSERT OR UPDATE OR DELETE
ON EXTRA
FOR EACH ROW
EXECUTE PROCEDURE calc_total_func();



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
    Huurobject."HuurobjectID_Benodigd",
    Voertuigtype."PrijsPerDag" as VoertuigPrijsPerDag
FROM Huurovereenkomst
INNER JOIN Extra
ON (Extra."Factuurnummer" = Huurovereenkomst."Factuurnummer")
INNER JOIN Huurobject
ON (Extra."HuurobjectID" = Huurobject."ID")
INNER JOIN Voertuig
ON (Huurovereenkomst."VoertuigID" = Voertuig."ID")
INNER JOIN Voertuigtype
ON (Voertuig."VoertuigtypeID" = Voertuigtype."ID");



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
    Huurobject."HuurobjectID_Benodigd",
    Voertuigtype."PrijsPerDag" as VoertuigPrijsPerDag
FROM Huurovereenkomst
INNER JOIN Extra
ON (Extra."Factuurnummer" = Huurovereenkomst."Factuurnummer")
INNER JOIN Huurobject
ON (Extra."HuurobjectID" = Huurobject."ID")
INNER JOIN Voertuig
ON (Huurovereenkomst."VoertuigID" = Voertuig."ID")
INNER JOIN Voertuigtype
ON (Voertuig."VoertuigtypeID" = Voertuigtype."ID");