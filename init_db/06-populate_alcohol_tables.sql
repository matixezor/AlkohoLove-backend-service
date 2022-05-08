INSERT INTO alcohol
VALUES (DEFAULT, 'Żywiec białe', 'piwo', 5.0, 'witbier',
        'Białe piwo pszeniczne z nutą kolendry. Wyróżna się lekkim i orzeźwiającym smakiem. Receptura piwa białego jest dziełem mistrzów żywieckiej szkoły piwowarskiej, którzy od pokoleń pracują w warzelniach arcyksiążęcych w Żywcu i Cieszynie.',
        1, 4.9, 'słomkowy', NULL, NULL, 18, 2.4, 11.6, 'top', FALSE, TRUE, '4-6', 'Żywiec', NULL, 'zywiec_biale'),
       (DEFAULT, 'Soplica Szlachetna Wódka', 'wódka', 4.0, 'czysta',
        'Jedna z najstarszych wódek w Polsce, to połączenie tradycji i nowoczesności. Wykonana jest z najwyższej klasy spirytusu produkowanego z wielkopolskiego zboża. W trakcie procesu technologicznego poddawana jest czterokrotnej aktywnej filtracji, dzięki czemu ma delikatny smak i zapach. Zastosowanie unikalnych metod oczyszczania spirytusu i zestawiania składników decyduje o jej szczególnym charakterze i harmonijnej kompozycji smakowo-zapachowej. To sprawdzony skład gwarantujący doskonałą jakość.',
        1, 40.0, 'przezroczysty', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Soplica', NULL, 'soplica_szlachetna_wodka');

INSERT INTO barcode
VALUES ('5900699104827', 1),
       ('5900471025319', 2);

INSERT INTO flavour
VALUES (DEFAULT, 'kolendra'),
       (DEFAULT, 'nuty korzenne');

INSERT INTO ingredient
VALUES (DEFAULT, 'mieszanka zbóż'),
       (DEFAULT, 'chmiel');

INSERT INTO food
VALUES (DEFAULT, 'białe mięso'),
       (DEFAULT, 'przekąski');

INSERT INTO alcohol_aroma
VALUES (1, 1);

INSERT INTO alcohol_ingredient
VALUES (1, 1);

INSERT INTO alcohol_food
VALUES (1, 1);
VALUES (1, 2);

INSERT INTO country
VALUES (DEFAULT, 'Polska'),
       (DEFAULT, 'Irlandia');

INSERT INTO region
VALUES (DEFAULT, 'Polska', 1),
       (DEFAULT, 'Irlandia', 2);
