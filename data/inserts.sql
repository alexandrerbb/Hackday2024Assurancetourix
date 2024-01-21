-- Data inserts.

PRAGMA foreign_keys = OFF;

BEGIN;

INSERT INTO "ticketresponseoption" ("name","description","start_exchange","ticket_response_id") 
    VALUES 
    ('declaration', 'Je souhaite déclarer un sinistre', 1, NULL),
    ('informations_contrat', 'Je souhaite d''avantages d''informations concernant mon contrat', 1, 
        NULL),
    ('informations_auto', 'Contrat d''assurance automobile', 0, 1),
    ('informations_habitation', 'Contrat d''assurance habitation', 0, 1),
    ('informations_vie', 'Contrat d''assurance vie', 0, 1),
    ('informations_sante', 'Contrat d''assurance santé', 0, 1),
    ('sinistre_coupable', 'Je suis fautif', 0, 0),
    ('sinistre_boisson', 'J''étais ivre', 0, 0),
    ('sinistre_autre', 'Autre', 0, 0)
    ;
    
INSERT INTO "customermessageresponse" ("id", "message","responds_to_id") 
    VALUES 
    (0, 'Je suis désolé d''apprendre que vous avez eu un accident.
Pour mieux vous assister veuillez choisir parmis les informations supplémentaires.', 'declaration'),

    (1, 'Pouvez-vous nous donner plus d''informations sur le type de contrat dont vous êtes le '||
'bénéficiaire ?', 
    'informations_contrat'),

    (2, 'Vous êtes bénéficiaire d''un contrat d''assurance chez ASSURTOUT, nous vous en remercions.
Nous couvrons vos arrière en cas de daummage matériel, le tout étant soumis à condition (voir '|| 
'votre contrat d''assurance).', 
'informations_auto'),

    (3, 'Notre conseiller vous recontactera dans les plus brefs delais afin de répondre à votre '||
'question.
Nous vous remercions de votre confiance.
Pour information, nous sommes ouvers du lundi au mercredi de 10h30 à 14h45 (hors pause dej et '||
'jours feriés).', 
'informations_habitation'),

    (4, 'Nous sommes très heureux que vous craigniez pour votre vie. Vous avez souscrit un '||
'contrat chez nous.
Nous couvrons tous les risques du quotidien (hors cause de décès naturelle). Nous ne couvrons pas'||
' les frais d''obsèques.', 
'informations_vie'),

    (5, 'D''après nos informations, vous n''êtes pas encore bénéficiaire d''un contrat d'''|| 
'assurance santé chez ASSURTOUT. 
Notre conseiller vous recontactera.', 'informations_sante'),

    (6, 'Vous êtes résponsable du sinstre, malheureusement les réparations seront à votre charge.', 
'sinistre_coupable'),

    (7, 'Comme stipulé dans votre contrat, vous êtes responsable du sinistre lorsque vous êtes en'||
'etat d''ivresse. 
Les réparations seront donc à votre charge.', 'sinistre_boisson'),

    (8, 'Malheureusement, aucun expert n''est aujourd''hui disponible afin de réaliser les ' ||
'constatations nécessaires. Nous vous recontacterons au besoin.', 'sinistre_autre')

 ;

COMMIT;

PRAGMA foreign_keys = ON;