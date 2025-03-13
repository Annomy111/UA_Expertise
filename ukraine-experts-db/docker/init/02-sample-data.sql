-- Sample data for Brussels organizations
INSERT INTO experts (name, type, city_id, description, is_diaspora, founding_year) 
VALUES 
('Promote Ukraine', 'organization', 
 (SELECT id FROM cities WHERE name = 'Brussels'), 
 'A non-profit advocacy and media hub established during the 2014 Revolution of Dignity. Became "Ukraine''s public voice in Brussels", organising rallies, humanitarian aid collection points, and advocacy events at EU institutions.', 
 TRUE, 2014);

INSERT INTO key_figures (organization_id, name, role, description)
VALUES 
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), 
 'Marta Barandiy', 
 'Founder & President', 
 'Ukrainian lawyer and civil society advocate who founded Promote Ukraine. Since Russia''s 2022 invasion, she has amplified the Ukrainian perspective in Brussels.');

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), 'advocacy'),
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), 'cultural_diplomacy');

INSERT INTO contacts (expert_id, contact_type, contact_value, is_primary)
VALUES 
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), 'website', 'promoteukraine.org', TRUE);

-- Association of Ukrainians in Belgium
INSERT INTO experts (name, type, city_id, description, is_diaspora, founding_year) 
VALUES 
('Association of Ukrainians in Belgium', 'organization', 
 (SELECT id FROM cities WHERE name = 'Brussels'), 
 'Umbrella organization representing the Ukrainian community in Belgium. Established post-WWII to unite Ukrainian displaced persons, it preserves Ukrainian identity and culture and coordinates community efforts.', 
 TRUE, 1948);

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Association of Ukrainians in Belgium'), 'community_support'),
((SELECT id FROM experts WHERE name = 'Association of Ukrainians in Belgium'), 'cultural_diplomacy');

-- BEforUkraine
INSERT INTO experts (name, type, city_id, description, is_diaspora, founding_year) 
VALUES 
('BEforUkraine', 'organization', 
 (SELECT id FROM cities WHERE name = 'Brussels'), 
 'A citizens'' initiative launched in March 2022 to deliver humanitarian aid and refugee support. Has transported medical equipment, ambulances, school buses and relocated hundreds of Ukrainian refugees to host families in Belgium.', 
 TRUE, 2022);

INSERT INTO key_figures (organization_id, name, role, description)
VALUES 
((SELECT id FROM experts WHERE name = 'BEforUkraine'), 
 'Thibault De Sadeleer', 
 'Co-founder', 
 'Belgian volunteer who helped establish the initiative in response to the 2022 invasion'),
((SELECT id FROM experts WHERE name = 'BEforUkraine'), 
 'Xavier Holst', 
 'Co-founder', 
 'Co-founder of the Belgian-Ukrainian humanitarian initiative');

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'BEforUkraine'), 'humanitarian');

INSERT INTO contacts (expert_id, contact_type, contact_value, is_primary)
VALUES 
((SELECT id FROM experts WHERE name = 'BEforUkraine'), 'website', 'beforua.be', TRUE);

-- Sample data for Berlin organizations
INSERT INTO experts (name, type, city_id, description, is_diaspora, founding_year) 
VALUES 
('Vitsche e.V.', 'organization', 
 (SELECT id FROM cities WHERE name = 'Berlin'), 
 'A youth-led Ukrainian activist community founded in January 2022. Stands for freedom and development of Ukraine, using protests, cultural diplomacy, and innovative campaigns.', 
 TRUE, 2022);

INSERT INTO key_figures (organization_id, name, role, description)
VALUES 
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 
 'Iryna Shulikina', 
 'Chairwoman & Executive Director', 
 'Leads the youth-driven Ukrainian diaspora NGO in Berlin'),
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 
 'Eva Yakubovska', 
 'Advocacy Lead', 
 'Coordinates advocacy efforts for the organization'),
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 
 'Krista-Marija Läbe', 
 'Spokesperson', 
 'Press spokesperson for the organization');

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 'political_mobilization'),
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 'cultural_diplomacy'),
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 'advocacy');

INSERT INTO contacts (expert_id, contact_type, contact_value, is_primary)
VALUES 
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 'website', 'vitsche.org', TRUE),
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 'social_media', 'instagram.com/vitsche_berlin', FALSE);

-- Alliance of Ukrainian Organizations
INSERT INTO experts (name, type, city_id, description, is_diaspora, founding_year) 
VALUES 
('Alliance of Ukrainian Organizations', 'organization', 
 (SELECT id FROM cities WHERE name = 'Berlin'), 
 'Formed in 2022 as a coalition uniting Berlin''s Ukrainian cultural, humanitarian, and political groups. Mobilizes the diaspora for demonstrations and advocacy, builds partnerships with German and international institutions.', 
 TRUE, 2022);

INSERT INTO key_figures (organization_id, name, role, description)
VALUES 
((SELECT id FROM experts WHERE name = 'Alliance of Ukrainian Organizations'), 
 'Nataliya Pryhornytska', 
 'Co-Founder', 
 'Co-founded the alliance to coordinate Ukrainian diaspora efforts in Berlin'),
((SELECT id FROM experts WHERE name = 'Alliance of Ukrainian Organizations'), 
 'Oleksandra Keudel', 
 'Co-Founder', 
 'Co-founded the alliance to strengthen Ukrainian voices in Germany');

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Alliance of Ukrainian Organizations'), 'advocacy'),
((SELECT id FROM experts WHERE name = 'Alliance of Ukrainian Organizations'), 'community_support');

-- Sample data for Paris organizations
INSERT INTO experts (name, type, city_id, description, is_diaspora, founding_year) 
VALUES 
('Union of Ukrainians in France', 'organization', 
 (SELECT id FROM cities WHERE name = 'Paris'), 
 'Founded in 1949 by Ukrainian refugees in France, it is the oldest Ukrainian diaspora association in Paris. Preserves Ukrainian heritage and represents the community nationally.', 
 TRUE, 1949);

INSERT INTO key_figures (organization_id, name, role, description)
VALUES 
((SELECT id FROM experts WHERE name = 'Union of Ukrainians in France'), 
 'Bohdan Bilot', 
 'President', 
 'Leads the historic Ukrainian diaspora organization in France'),
((SELECT id FROM experts WHERE name = 'Union of Ukrainians in France'), 
 'Volodymyr Kogutyak', 
 'Vice-President', 
 'Vice-President of the Union and also affiliated with the Ukrainian World Congress');

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Union of Ukrainians in France'), 'advocacy'),
((SELECT id FROM experts WHERE name = 'Union of Ukrainians in France'), 'community_support'),
((SELECT id FROM experts WHERE name = 'Union of Ukrainians in France'), 'cultural_diplomacy');

INSERT INTO contacts (expert_id, contact_type, contact_value, is_primary)
VALUES 
((SELECT id FROM experts WHERE name = 'Union of Ukrainians in France'), 'website', 'uduf.fr', TRUE);

-- Association of Ukrainian Women in France
INSERT INTO experts (name, type, city_id, description, is_diaspora, founding_year) 
VALUES 
('Association des Femmes Ukrainiennes en France', 'organization', 
 (SELECT id FROM cities WHERE name = 'Paris'), 
 'A diaspora women-led charity focusing on humanitarian aid to Ukraine. Since 2022, it has sent critical supplies: ambulances, generators, medical gear, food and clothing to war zones.', 
 TRUE, NULL);

INSERT INTO key_figures (organization_id, name, role, description)
VALUES 
((SELECT id FROM experts WHERE name = 'Association des Femmes Ukrainiennes en France'), 
 'Nadia Myhal', 
 'President', 
 'Leads the Ukrainian women''s association in France');

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Association des Femmes Ukrainiennes en France'), 'humanitarian'),
((SELECT id FROM experts WHERE name = 'Association des Femmes Ukrainiennes en France'), 'community_support');

-- Sample data for Warsaw organizations
INSERT INTO experts (name, type, city_id, description, is_diaspora, founding_year) 
VALUES 
('Fundacja "Nasz Wybór"', 'organization', 
 (SELECT id FROM cities WHERE name = 'Warsaw'), 
 'Founded in 2009 by Ukrainians and Polish friends to support Ukrainian migrants in Poland. Operates the Ukrainian House in Warsaw, a cultural and information center offering legal advice, job assistance, language courses, and community events for Ukrainians.', 
 TRUE, 2009);

INSERT INTO key_figures (organization_id, name, role, description)
VALUES 
((SELECT id FROM experts WHERE name = 'Fundacja "Nasz Wybór"'), 
 'Myroslava Keryk', 
 'President', 
 'Ukrainian historian and community leader who heads the foundation');

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Fundacja "Nasz Wybór"'), 'community_support'),
((SELECT id FROM experts WHERE name = 'Fundacja "Nasz Wybór"'), 'integration'),
((SELECT id FROM experts WHERE name = 'Fundacja "Nasz Wybór"'), 'cultural_diplomacy');

INSERT INTO contacts (expert_id, contact_type, contact_value, is_primary)
VALUES 
((SELECT id FROM experts WHERE name = 'Fundacja "Nasz Wybór"'), 'website', 'naszwybor.org.pl', TRUE),
((SELECT id FROM experts WHERE name = 'Fundacja "Nasz Wybór"'), 'website', 'ukrainskidom.pl', FALSE);

-- Stand With Ukraine / Euromaidan-Warszawa
INSERT INTO experts (name, type, city_id, description, is_diaspora, founding_year) 
VALUES 
('Stand With Ukraine Foundation', 'organization', 
 (SELECT id FROM cities WHERE name = 'Warsaw'), 
 'A grassroots civil movement of Ukrainians in Warsaw born out of the 2013–14 Maidan. Advocates for Ukraine''s freedom and EU integration, and organizes major solidarity actions in Poland.', 
 TRUE, 2014);

INSERT INTO key_figures (organization_id, name, role, description)
VALUES 
((SELECT id FROM experts WHERE name = 'Stand With Ukraine Foundation'), 
 'Natalia Panchenko', 
 'Founder & Leader', 
 'Founded and leads the diaspora activist movement and charity');

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Stand With Ukraine Foundation'), 'advocacy'),
((SELECT id FROM experts WHERE name = 'Stand With Ukraine Foundation'), 'humanitarian'),
((SELECT id FROM experts WHERE name = 'Stand With Ukraine Foundation'), 'political_mobilization');

INSERT INTO contacts (expert_id, contact_type, contact_value, is_primary)
VALUES 
((SELECT id FROM experts WHERE name = 'Stand With Ukraine Foundation'), 'social_media', 'facebook.com/EuromaidanWarszawa', TRUE);

-- Sample data for individual experts
INSERT INTO experts (name, type, title, affiliation, city_id, description, is_diaspora) 
VALUES 
('Amanda Paul', 'individual', 
 'Senior Policy Analyst', 
 'European Policy Centre (EPC)', 
 (SELECT id FROM cities WHERE name = 'Brussels'), 
 'Senior analyst focusing on Europe''s Eastern flank (Ukraine, Moldova, South Caucasus) and Black Sea security; leads EPC''s "Ukraine''s European Future" project', 
 FALSE);

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Amanda Paul'), 'policy_analysis'),
((SELECT id FROM experts WHERE name = 'Amanda Paul'), 'research');

-- Dr. Olena Prystayko
INSERT INTO experts (name, type, title, affiliation, city_id, description, is_diaspora) 
VALUES 
('Dr. Olena Prystayko', 'individual', 
 'Executive Director', 
 'Ukrainian Think Tanks Liaison Office in Brussels', 
 (SELECT id FROM cities WHERE name = 'Brussels'), 
 'Heads the Brussels liaison office that connects Ukrainian think tanks with EU policymakers. Former Council of Europe officer; co-author of Freedom House''s Nations in Transit report on Ukraine', 
 TRUE);

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Dr. Olena Prystayko'), 'policy_analysis'),
((SELECT id FROM experts WHERE name = 'Dr. Olena Prystayko'), 'advocacy');

-- Prof. Gwendolyn Sasse
INSERT INTO experts (name, type, title, affiliation, city_id, description, is_diaspora) 
VALUES 
('Prof. Gwendolyn Sasse', 'individual', 
 'Director', 
 'Centre for East European and International Studies (ZOiS)', 
 (SELECT id FROM cities WHERE name = 'Berlin'), 
 'Political scientist leading ZOiS (Berlin). Her research focuses on Eastern Europe – particularly Ukrainian politics and society – and EU enlargement. Author of Russia''s War Against Ukraine (2023) and frequent commentator on Ukraine in European media', 
 FALSE);

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Prof. Gwendolyn Sasse'), 'research'),
((SELECT id FROM experts WHERE name = 'Prof. Gwendolyn Sasse'), 'policy_analysis');

-- Tatiana Kastueva-Jean
INSERT INTO experts (name, type, title, affiliation, city_id, description, is_diaspora) 
VALUES 
('Tatiana Kastueva-Jean', 'individual', 
 'Director', 
 'Russia/New Independent States Center, IFRI', 
 (SELECT id FROM cities WHERE name = 'Paris'), 
 'Political scientist heading the Russia/NIS Center at the French Institute of International Relations in Paris. Research areas include Russia''s domestic and foreign policy and Ukraine. Provides analysis on Russia''s war in Ukraine and its global implications in French and international media', 
 FALSE);

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Tatiana Kastueva-Jean'), 'research'),
((SELECT id FROM experts WHERE name = 'Tatiana Kastueva-Jean'), 'policy_analysis');

-- Wojciech Konończuk
INSERT INTO experts (name, type, title, affiliation, city_id, description, is_diaspora) 
VALUES 
('Wojciech Konończuk', 'individual', 
 'Director', 
 'Centre for Eastern Studies (OSW)', 
 (SELECT id FROM cities WHERE name = 'Warsaw'), 
 'Seasoned analyst heading OSW in Warsaw. Formerly led OSW''s department on Ukraine, Belarus, and Moldova, he specializes in the political and economic dynamics of Eastern Europe and Russia–Ukraine relations. Regularly briefs Polish authorities and media on developments in Ukraine', 
 FALSE);

INSERT INTO expert_focus_areas (expert_id, focus_area)
VALUES 
((SELECT id FROM experts WHERE name = 'Wojciech Konończuk'), 'research'),
((SELECT id FROM experts WHERE name = 'Wojciech Konończuk'), 'policy_analysis');

-- Add some tags
INSERT INTO tags (name) VALUES 
('EU integration'), 
('NATO'), 
('humanitarian aid'), 
('diaspora'), 
('civil society'), 
('advocacy'), 
('cultural diplomacy'), 
('refugee support'), 
('policy analysis'), 
('Ukraine-EU relations');

-- Add tags to experts
INSERT INTO expert_tags (expert_id, tag_id) VALUES
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), (SELECT id FROM tags WHERE name = 'EU integration')),
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), (SELECT id FROM tags WHERE name = 'advocacy')),
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), (SELECT id FROM tags WHERE name = 'diaspora')),
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), (SELECT id FROM tags WHERE name = 'civil society')),

((SELECT id FROM experts WHERE name = 'BEforUkraine'), (SELECT id FROM tags WHERE name = 'humanitarian aid')),
((SELECT id FROM experts WHERE name = 'BEforUkraine'), (SELECT id FROM tags WHERE name = 'refugee support')),

((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), (SELECT id FROM tags WHERE name = 'diaspora')),
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), (SELECT id FROM tags WHERE name = 'advocacy')),
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), (SELECT id FROM tags WHERE name = 'cultural diplomacy')),

((SELECT id FROM experts WHERE name = 'Union of Ukrainians in France'), (SELECT id FROM tags WHERE name = 'diaspora')),
((SELECT id FROM experts WHERE name = 'Union of Ukrainians in France'), (SELECT id FROM tags WHERE name = 'cultural diplomacy')),

((SELECT id FROM experts WHERE name = 'Stand With Ukraine Foundation'), (SELECT id FROM tags WHERE name = 'EU integration')),
((SELECT id FROM experts WHERE name = 'Stand With Ukraine Foundation'), (SELECT id FROM tags WHERE name = 'advocacy')),
((SELECT id FROM experts WHERE name = 'Stand With Ukraine Foundation'), (SELECT id FROM tags WHERE name = 'humanitarian aid')),

((SELECT id FROM experts WHERE name = 'Amanda Paul'), (SELECT id FROM tags WHERE name = 'policy analysis')),
((SELECT id FROM experts WHERE name = 'Amanda Paul'), (SELECT id FROM tags WHERE name = 'Ukraine-EU relations')),

((SELECT id FROM experts WHERE name = 'Dr. Olena Prystayko'), (SELECT id FROM tags WHERE name = 'policy analysis')),
((SELECT id FROM experts WHERE name = 'Dr. Olena Prystayko'), (SELECT id FROM tags WHERE name = 'Ukraine-EU relations')),
((SELECT id FROM experts WHERE name = 'Dr. Olena Prystayko'), (SELECT id FROM tags WHERE name = 'civil society')),

((SELECT id FROM experts WHERE name = 'Prof. Gwendolyn Sasse'), (SELECT id FROM tags WHERE name = 'policy analysis')),
((SELECT id FROM experts WHERE name = 'Wojciech Konończuk'), (SELECT id FROM tags WHERE name = 'policy analysis'));

-- Add some links
INSERT INTO links (expert_id, url, title, description) VALUES
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), 'https://promoteukraine.org', 'Official Website', 'Official website of Promote Ukraine'),
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), 'https://www.facebook.com/PromoteUkraine', 'Facebook Page', 'Facebook page of Promote Ukraine'),

((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 'https://vitsche.org', 'Official Website', 'Official website of Vitsche e.V.'),
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 'https://www.instagram.com/vitsche_berlin', 'Instagram', 'Instagram account of Vitsche Berlin'),

((SELECT id FROM experts WHERE name = 'Fundacja "Nasz Wybór"'), 'https://naszwybor.org.pl', 'Official Website', 'Official website of Fundacja "Nasz Wybór"'),
((SELECT id FROM experts WHERE name = 'Fundacja "Nasz Wybór"'), 'https://ukrainskidom.pl', 'Ukrainian House in Warsaw', 'Website of the Ukrainian House in Warsaw operated by the foundation'),

((SELECT id FROM experts WHERE name = 'Amanda Paul'), 'https://www.epc.eu/en/staff/Amanda-Paul~1c1a94', 'EPC Profile', 'Amanda Paul''s profile at the European Policy Centre'),

((SELECT id FROM experts WHERE name = 'Prof. Gwendolyn Sasse'), 'https://www.zois-berlin.de/en/about-us/team/prof-dr-gwendolyn-sasse', 'ZOiS Profile', 'Prof. Gwendolyn Sasse''s profile at the Centre for East European and International Studies');

-- Add some activities
INSERT INTO activities (expert_id, title, description, date_start, date_end) VALUES
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), 'European Advocacy Forum', 'Annual forum bringing together Ukrainian civil society representatives and EU policymakers', '2022-06-15', '2022-06-16'),
((SELECT id FROM experts WHERE name = 'Promote Ukraine'), 'Stand With Ukraine Rally', 'Major demonstration in Brussels in support of Ukraine following the full-scale invasion', '2022-02-24', '2022-02-24'),

((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 'Weekly Protests at Brandenburg Gate', 'Regular demonstrations in Berlin to maintain public attention on Ukraine''s struggle', '2022-02-27', NULL),
((SELECT id FROM experts WHERE name = 'Vitsche e.V.'), 'Ukrainian Culture Days', 'Festival showcasing Ukrainian art, music, and cuisine to Berlin audiences', '2022-08-24', '2022-08-26'),

((SELECT id FROM experts WHERE name = 'Union of Ukrainians in France'), 'Rally for Ukraine''s NATO Accession', 'Demonstration in Paris advocating for Ukraine''s path to NATO membership', '2023-07-11', '2023-07-11'),

((SELECT id FROM experts WHERE name = 'Stand With Ukraine Foundation'), '"International Genocide Trade Fair" Performance', 'Creative protest in Warsaw urging the EU to embargo all trade with Russia', '2024-04-10', '2024-04-10'),

((SELECT id FROM experts WHERE name = 'Prof. Gwendolyn Sasse'), 'Publication: Russia''s War Against Ukraine', 'Released book analyzing the Russian invasion and its implications', '2023-03-01', NULL),

((SELECT id FROM experts WHERE name = 'Wojciech Konończuk'), 'OSW Analysis on Ukraine''s EU Accession Process', 'Published comprehensive analysis of Ukraine''s path to EU membership', '2023-06-23', NULL); 