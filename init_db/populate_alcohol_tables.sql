INSERT INTO alcohol
VALUES (DEFAULT, 'Żywiec białe', 'beer', 5.0, 'witbier',
        'Białe piwo pszeniczne z nutą kolendry. Wyróżna się lekkim i orzeźwiającym smakiem. Receptura piwa białego jest dziełem mistrzów żywieckiej szkoły piwowarskiej, którzy od pokoleń pracują w warzelniach arcyksiążęcych w Żywcu i Cieszynie.',
        1, 4.9, 'słomkowy', NULL, 18, 2.4, 11.6, 'top', FALSE, TRUE, '4-6', 'Żywiec', NULL, NULL),
       (DEFAULT, 'Soplica Szlachetna Wódka', 'vodka', 4.0, 'czysta',
        'Jedna z najstarszych wódek w Polsce, to połączenie tradycji i nowoczesności. Wykonana jest z najwyższej klasy spirytusu produkowanego z wielkopolskiego zboża. W trakcie procesu technologicznego poddawana jest czterokrotnej aktywnej filtracji, dzięki czemu ma delikatny smak i zapach. Zastosowanie unikalnych metod oczyszczania spirytusu i zestawiania składników decyduje o jej szczególnym charakterze i harmonijnej kompozycji smakowo-zapachowej. To sprawdzony skład gwarantujący doskonałą jakość.',
        1,
        40.0, 'przezroczysty', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Soplica', NULL, NULL);


INSERT INTO bar_code
VALUES ('5900699104827', 1),
       ('5900471025319', 2);

INSERT INTO aroma
VALUES (DEFAULT, 'kolendra');

INSERT INTO ingredient
VALUES (DEFAULT, 'mieszanka zbóż');

INSERT INTO food
VALUES (DEFAULT, 'białe mięso'),
       (DEFAULT, 'przekąski');

INSERT INTO alcohol_aroma
VALUES (1, 1);

INSERT INTO alcohol_ingredient
VALUES (1, 1);

INSERT INTO alcohol_food_pairing
VALUES (1, 1);
VALUES (1, 2);

INSERT INTO country
VALUES (DEFAULT, 'Polska');

INSERT INTO region
VALUES (DEFAULT, 'Polska', 1);
