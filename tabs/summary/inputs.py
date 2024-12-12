import dash_bootstrap_components as dbc
from dash import html

from tabs.summary.input_layout_utils import generate_card, run_button, generate_card_card, form_input
from tabs.summary.summary_tab import cities

input_location = form_input('Location', cities[0], options=cities, multi=False)
location_card = generate_card(
    'Location',
    [input_location]
)

# Income
input_income = form_input('Income', 120000, 1000)
income_card = generate_card(
    'Income',
    [input_income]
)

# Housing
property_types = ['MULTI_FAMILY', 'SINGLE_FAMILY', 'MANUFACTURED', 'CONDO', 'TOWNHOUSE', 'APARTMENT']
input_property_type = form_input('Property Type', property_types[1], options=property_types, )
rent_or_buy = ['RENT', 'BUY']
rent_or_buy_type = form_input('Rent or Buy', rent_or_buy[0], options=rent_or_buy, )

# input_income = form_input('Income', 70000, 1000),
housing_card = generate_card(
    'Housing',
    [input_property_type, rent_or_buy_type],
)

# Tax
filing_status = ['Single', 'Married filing jointly', 'Married filing separately', 'Head of household']
input_filling_status = form_input('Filing Status', filing_status[0], options=filing_status)
input_property_value = form_input('Property Value', 400_000, step=1000)
input_number_of_kid = form_input('Number of Kids', placeholder=1)
tax_card = generate_card(
    'Tax Estimate',
    [
        input_filling_status,
        input_property_value,
        input_number_of_kid,
    ]
)

# Income
occupations = ['Accountants and Auditors', 'Administrative Law Judges, Adjudicators, and Hearing Officers',
               'Administrative Services Managers',
               'Adult Basic Education, Adult Secondary Education, and English as a Second Language Instructors',
               'Advertising Sales Agents', 'Advertising and Promotions Managers', 'Aircraft Cargo Handling Supervisors',
               'Aircraft Mechanics and Service Technicians', 'Aircraft Service Attendants',
               'Amusement and Recreation Attendants', 'Animal Caretakers', 'Animal Control Workers', 'Animal Trainers',
               'Architects, Except Landscape and Naval', 'Architectural and Civil Drafters',
               'Architectural and Engineering Managers', 'Art Directors',
               'Art, Drama, and Music Teachers, Postsecondary', 'Artists and Related Workers, All Other',
               'Athletic Trainers', 'Atmospheric and Space Scientists', 'Audio and Video Technicians',
               'Automotive Body and Related Repairers', 'Automotive Service Technicians and Mechanics',
               'Automotive and Watercraft Service Attendants', 'Baggage Porters and Bellhops', 'Bakers', 'Bartenders',
               'Bill and Account Collectors', 'Biological Scientists, All Other', 'Biological Technicians',
               'Bookkeeping, Accounting, and Auditing Clerks', 'Brickmasons and Blockmasons',
               'Broadcast Announcers and Radio Disc Jockeys', 'Broadcast Technicians', 'Brokerage Clerks',
               'Budget Analysts', 'Bus Drivers, School', 'Bus Drivers, Transit and Intercity',
               'Bus and Truck Mechanics and Diesel Engine Specialists', 'Business Operations Specialists, All Other',
               'Butchers and Meat Cutters', 'Buyers and Purchasing Agents', 'Cabinetmakers and Bench Carpenters',
               'Calibration Technologists and Technicians', 'Camera Operators, Television, Video, and Film',
               'Cardiologists', 'Cardiovascular Technologists and Technicians',
               'Career/Technical Education Teachers, Postsecondary', 'Cargo and Freight Agents', 'Carpenters',
               'Carpet Installers', 'Cartographers and Photogrammetrists', 'Cashiers',
               'Cement Masons and Concrete Finishers', 'Chefs and Head Cooks', 'Chemical Technicians', 'Chemists',
               'Chief Executives', 'Child, Family, and School Social Workers', 'Childcare Workers', 'Chiropractors',
               'Civil Engineering Technologists and Technicians', 'Civil Engineers',
               'Claims Adjusters, Examiners, and Investigators', 'Cleaners of Vehicles and Equipment',
               'Cleaning, Washing, and Metal Pickling Equipment Operators and Tenders', 'Clergy',
               'Clinical Laboratory Technologists and Technicians', 'Clinical and Counseling Psychologists',
               'Coaches and Scouts', 'Coating, Painting, and Spraying Machine Setters, Operators, and Tenders',
               'Coin, Vending, and Amusement Machine Servicers and Repairers', 'Commercial Pilots',
               'Community Health Workers', 'Community and Social Service Specialists, All Other',
               'Compensation and Benefits Managers', 'Compensation, Benefits, and Job Analysis Specialists',
               'Compliance Officers', 'Computer Hardware Engineers', 'Computer Network Architects',
               'Computer Network Support Specialists', 'Computer Numerically Controlled Tool Operators',
               'Computer Occupations, All Other', 'Computer Programmers', 'Computer Science Teachers, Postsecondary',
               'Computer Systems Analysts', 'Computer User Support Specialists',
               'Computer and Information Systems Managers', 'Computer, Automated Teller, and Office Machine Repairers',
               'Concierges', 'Construction Laborers', 'Construction Managers', 'Construction and Building Inspectors',
               'Control and Valve Installers and Repairers, Except Mechanical Door', 'Cooks, Fast Food',
               'Cooks, Institution and Cafeteria', 'Cooks, Restaurant', 'Cooks, Short Order',
               'Correctional Officers and Jailers', 'Cost Estimators', 'Counselors, All Other',
               'Counter and Rental Clerks', 'Couriers and Messengers', 'Court, Municipal, and License Clerks',
               'Credit Analysts', 'Credit Authorizers, Checkers, and Clerks', 'Credit Counselors',
               'Crossing Guards and Flaggers',
               'Crushing, Grinding, and Polishing Machine Setters, Operators, and Tenders', 'Curators',
               'Customer Service Representatives', 'Cutting and Slicing Machine Setters, Operators, and Tenders',
               'Cutting, Punching, and Press Machine Setters, Operators, and Tenders, Metal and Plastic',
               'Data Entry Keyers', 'Data Scientists', 'Database Administrators', 'Database Architects',
               'Demonstrators and Product Promoters', 'Dental Assistants', 'Dental Hygienists',
               'Dental Laboratory Technicians', 'Dentists, General', 'Detectives and Criminal Investigators',
               'Diagnostic Medical Sonographers', 'Dietetic Technicians', 'Dietitians and Nutritionists',
               'Dining Room and Cafeteria Attendants and Bartender Helpers', 'Dishwashers',
               'Dispatchers, Except Police, Fire, and Ambulance', 'Drafters, All Other', 'Driver/Sales Workers',
               'Drywall and Ceiling Tile Installers', 'Earth Drillers, Except Oil and Gas', 'Editors',
               'Education Administrators, All Other', 'Education Administrators, Kindergarten through Secondary',
               'Education Administrators, Postsecondary', 'Education Teachers, Postsecondary',
               'Education and Childcare Administrators, Preschool and Daycare',
               'Educational Instruction and Library Workers, All Other',
               'Educational, Guidance, and Career Counselors and Advisors',
               'Electric Motor, Power Tool, and Related Repairers', 'Electrical Engineers',
               'Electrical Power-Line Installers and Repairers',
               'Electrical and Electronic Engineering Technologists and Technicians',
               'Electrical and Electronics Drafters',
               'Electrical and Electronics Repairers, Commercial and Industrial Equipment', 'Electricians',
               'Electro-Mechanical and Mechatronics Technologists and Technicians',
               'Electronic Equipment Installers and Repairers, Motor Vehicles',
               'Electronics Engineers, Except Computer', 'Elementary School Teachers, Except Special Education',
               'Eligibility Interviewers, Government Programs', 'Emergency Management Directors',
               'Emergency Medical Technicians', 'Engineering Technologists and Technicians, Except Drafters, All Other',
               'Engineers, All Other', 'Entertainment and Recreation Managers, Except Gambling',
               'Environmental Engineering Technologists and Technicians', 'Environmental Engineers',
               'Environmental Science and Protection Technicians, Including Health',
               'Environmental Scientists and Specialists, Including Health',
               'Executive Secretaries and Executive Administrative Assistants',
               'Exercise Trainers and Group Fitness Instructors',
               'Extruding and Drawing Machine Setters, Operators, and Tenders, Metal and Plastic',
               'Facilities Managers', 'Family Medicine Physicians',
               'Farmworkers and Laborers, Crop, Nursery, and Greenhouse',
               'Farmworkers, Farm, Ranch, and Aquacultural Animals', 'Fast Food and Counter Workers', 'File Clerks',
               'Film and Video Editors', 'Financial Clerks, All Other', 'Financial Examiners', 'Financial Managers',
               'Financial Risk Specialists', 'Financial Specialists, All Other', 'Financial and Investment Analysts',
               'Fire Inspectors and Investigators', 'Firefighters',
               'First-Line Supervisors of Construction Trades and Extraction Workers',
               'First-Line Supervisors of Correctional Officers',
               'First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services',
               'First-Line Supervisors of Farming, Fishing, and Forestry Workers',
               'First-Line Supervisors of Firefighting and Prevention Workers',
               'First-Line Supervisors of Food Preparation and Serving Workers',
               'First-Line Supervisors of Housekeeping and Janitorial Workers',
               'First-Line Supervisors of Landscaping, Lawn Service, and Groundskeeping Workers',
               'First-Line Supervisors of Mechanics, Installers, and Repairers',
               'First-Line Supervisors of Non-Retail Sales Workers',
               'First-Line Supervisors of Office and Administrative Support Workers',
               'First-Line Supervisors of Personal Service Workers', 'First-Line Supervisors of Police and Detectives',
               'First-Line Supervisors of Production and Operating Workers',
               'First-Line Supervisors of Protective Service Workers, All Other',
               'First-Line Supervisors of Retail Sales Workers', 'First-Line Supervisors of Security Workers',
               'First-Line Supervisors of Transportation and Material Moving Workers, Except Aircraft Cargo Handling Supervisors',
               'Flight Attendants', 'Floor Layers, Except Carpet, Wood, and Hard Tiles', 'Floral Designers',
               'Food Batchmakers', 'Food Preparation Workers',
               'Food Preparation and Serving Related Workers, All Other', 'Food Processing Workers, All Other',
               'Food Servers, Nonrestaurant', 'Food Service Managers',
               'Food and Tobacco Roasting, Baking, and Drying Machine Operators and Tenders',
               'Forensic Science Technicians', 'Forest and Conservation Technicians', 'Fundraisers',
               'Fundraising Managers', 'Funeral Attendants', 'Funeral Home Managers',
               'Furnace, Kiln, Oven, Drier, and Kettle Operators and Tenders', 'Furniture Finishers',
               'General Internal Medicine Physicians', 'General and Operations Managers',
               'Geoscientists, Except Hydrologists and Geographers', 'Glaziers', 'Graphic Designers',
               'Grinding, Lapping, Polishing, and Buffing Machine Tool Setters, Operators, and Tenders, Metal and Plastic',
               'Hairdressers, Hairstylists, and Cosmetologists', 'Hazardous Materials Removal Workers',
               'Health Education Specialists', 'Health Specialties Teachers, Postsecondary',
               'Health Technologists and Technicians, All Other',
               'Health and Safety Engineers, Except Mining Safety Engineers and Inspectors',
               'Healthcare Practitioners and Technical Workers, All Other', 'Healthcare Social Workers',
               'Healthcare Support Workers, All Other',
               'Heating, Air Conditioning, and Refrigeration Mechanics and Installers',
               'Heavy and Tractor-Trailer Truck Drivers', 'Helpers, Construction Trades, All Other',
               'Helpers--Brickmasons, Blockmasons, Stonemasons, and Tile and Marble Setters', 'Helpers--Carpenters',
               'Helpers--Electricians', 'Helpers--Installation, Maintenance, and Repair Workers',
               'Helpers--Pipelayers, Plumbers, Pipefitters, and Steamfitters', 'Helpers--Production Workers',
               'Highway Maintenance Workers', 'Home Appliance Repairers', 'Home Health and Personal Care Aides',
               'Hosts and Hostesses, Restaurant, Lounge, and Coffee Shop', 'Hotel, Motel, and Resort Desk Clerks',
               'Human Resources Assistants, Except Payroll and Timekeeping', 'Human Resources Managers',
               'Human Resources Specialists', 'Industrial Engineering Technologists and Technicians',
               'Industrial Engineers', 'Industrial Machinery Mechanics', 'Industrial Production Managers',
               'Industrial Truck and Tractor Operators', 'Information Security Analysts',
               'Information and Record Clerks, All Other', 'Inspectors, Testers, Sorters, Samplers, and Weighers',
               'Installation, Maintenance, and Repair Workers, All Other', 'Instructional Coordinators',
               'Insulation Workers, Mechanical', 'Insurance Claims and Policy Processing Clerks',
               'Insurance Sales Agents', 'Insurance Underwriters', 'Interior Designers', 'Interpreters and Translators',
               'Interviewers, Except Eligibility and Loan',
               'Janitors and Cleaners, Except Maids and Housekeeping Cleaners',
               'Kindergarten Teachers, Except Special Education', 'Labor Relations Specialists',
               'Laborers and Freight, Stock, and Material Movers, Hand', 'Landscape Architects',
               'Landscaping and Groundskeeping Workers', 'Laundry and Dry-Cleaning Workers', 'Lawyers',
               'Legal Secretaries and Administrative Assistants', 'Legal Support Workers, All Other',
               'Librarians and Media Collections Specialists', 'Library Assistants, Clerical', 'Library Technicians',
               'Licensed Practical and Licensed Vocational Nurses',
               'Life, Physical, and Social Science Technicians, All Other',
               'Lifeguards, Ski Patrol, and Other Recreational Protective Service Workers', 'Light Truck Drivers',
               'Loan Interviewers and Clerks', 'Loan Officers', 'Locker Room, Coatroom, and Dressing Room Attendants',
               'Locksmiths and Safe Repairers', 'Lodging Managers', 'Logisticians', 'Machine Feeders and Offbearers',
               'Machinists', 'Magnetic Resonance Imaging Technologists', 'Maids and Housekeeping Cleaners',
               'Mail Clerks and Mail Machine Operators, Except Postal Service', 'Maintenance Workers, Machinery',
               'Maintenance and Repair Workers, General', 'Management Analysts', 'Managers, All Other',
               'Manicurists and Pedicurists', 'Market Research Analysts and Marketing Specialists',
               'Marketing Managers', 'Marriage and Family Therapists', 'Massage Therapists',
               'Material Moving Workers, All Other', 'Meat, Poultry, and Fish Cutters and Trimmers',
               'Mechanical Drafters', 'Mechanical Engineering Technologists and Technicians', 'Mechanical Engineers',
               'Media and Communication Equipment Workers, All Other', 'Media and Communication Workers, All Other',
               'Medical Assistants', 'Medical Equipment Preparers', 'Medical Equipment Repairers',
               'Medical Records Specialists', 'Medical Scientists, Except Epidemiologists',
               'Medical Secretaries and Administrative Assistants', 'Medical Transcriptionists',
               'Medical and Health Services Managers', 'Meeting, Convention, and Event Planners',
               'Mental Health and Substance Abuse Social Workers', 'Merchandise Displayers and Window Trimmers',
               'Meter Readers, Utilities', 'Middle School Teachers, Except Special and Career/Technical Education',
               'Miscellaneous Assemblers and Fabricators', 'Miscellaneous Construction and Related Workers',
               'Mixing and Blending Machine Setters, Operators, and Tenders',
               'Mobile Heavy Equipment Mechanics, Except Engines',
               'Molders, Shapers, and Casters, Except Metal and Plastic',
               'Molding, Coremaking, and Casting Machine Setters, Operators, and Tenders, Metal and Plastic',
               'Morticians, Undertakers, and Funeral Arrangers', 'Motor Vehicle Operators, All Other',
               'Museum Technicians and Conservators', 'Musicians and Singers', 'Natural Sciences Managers',
               'Network and Computer Systems Administrators', 'New Accounts Clerks',
               'News Analysts, Reporters, and Journalists', 'Nuclear Medicine Technologists', 'Nurse Practitioners',
               'Nursing Assistants', 'Nursing Instructors and Teachers, Postsecondary',
               'Occupational Health and Safety Specialists', 'Occupational Health and Safety Technicians',
               'Occupational Therapists', 'Occupational Therapy Assistants', 'Office Clerks, General',
               'Office Machine Operators, Except Computer', 'Office and Administrative Support Workers, All Other',
               'Operating Engineers and Other Construction Equipment Operators', 'Operations Research Analysts',
               'Ophthalmic Laboratory Technicians', 'Ophthalmic Medical Technicians', 'Opticians, Dispensing',
               'Optometrists', 'Order Clerks', 'Orderlies', 'Orthotists and Prosthetists',
               'Outdoor Power Equipment and Other Small Engine Mechanics',
               'Packaging and Filling Machine Operators and Tenders', 'Packers and Packagers, Hand',
               'Painters, Construction and Maintenance', 'Paralegals and Legal Assistants', 'Paramedics',
               'Parking Attendants', 'Parking Enforcement Workers', 'Parts Salespersons', 'Passenger Attendants',
               'Paving, Surfacing, and Tamping Equipment Operators', 'Payroll and Timekeeping Clerks',
               'Personal Care and Service Workers, All Other', 'Personal Financial Advisors', 'Pest Control Workers',
               'Pesticide Handlers, Sprayers, and Applicators, Vegetation', 'Pharmacists', 'Pharmacy Aides',
               'Pharmacy Technicians', 'Phlebotomists', 'Photographers', 'Physical Scientists, All Other',
               'Physical Therapist Aides', 'Physical Therapist Assistants', 'Physical Therapists',
               'Physician Assistants', 'Physicians, All Other', 'Pipelayers', 'Plant and System Operators, All Other',
               'Plasterers and Stucco Masons', 'Plating Machine Setters, Operators, and Tenders, Metal and Plastic',
               'Plumbers, Pipefitters, and Steamfitters', "Police and Sheriff's Patrol Officers",
               'Postal Service Clerks', 'Postal Service Mail Carriers',
               'Postal Service Mail Sorters, Processors, and Processing Machine Operators', 'Power Plant Operators',
               'Prepress Technicians and Workers', 'Preschool Teachers, Except Special Education',
               'Pressers, Textile, Garment, and Related Materials', 'Print Binding and Finishing Workers',
               'Printing Press Operators', 'Private Detectives and Investigators',
               'Probation Officers and Correctional Treatment Specialists', 'Procurement Clerks',
               'Producers and Directors', 'Production Workers, All Other',
               'Production, Planning, and Expediting Clerks', 'Project Management Specialists',
               'Property Appraisers and Assessors', 'Property, Real Estate, and Community Association Managers',
               'Protective Service Workers, All Other', 'Psychiatric Technicians', 'Psychiatrists',
               'Psychologists, All Other', 'Public Relations Managers', 'Public Relations Specialists',
               'Public Safety Telecommunicators', 'Purchasing Managers',
               'Radio, Cellular, and Tower Equipment Installers and Repairers',
               'Radiologic Technologists and Technicians', 'Real Estate Sales Agents',
               'Receptionists and Information Clerks', 'Recreation Workers', 'Recreational Therapists',
               'Refuse and Recyclable Material Collectors', 'Registered Nurses', 'Rehabilitation Counselors',
               'Reservation and Transportation Ticket Agents and Travel Clerks', 'Residential Advisors',
               'Respiratory Therapists', 'Retail Salespersons', 'Riggers', 'Roofers', 'Sales Engineers',
               'Sales Managers',
               'Sales Representatives of Services, Except Advertising, Insurance, Financial Services, and Travel',
               'Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products',
               'Sales Representatives, Wholesale and Manufacturing, Technical and Scientific Products',
               'Sales and Related Workers, All Other', 'School Psychologists',
               'Secondary School Teachers, Except Special and Career/Technical Education',
               'Secretaries and Administrative Assistants, Except Legal, Medical, and Executive',
               'Securities, Commodities, and Financial Services Sales Agents', 'Security Guards',
               'Security and Fire Alarm Systems Installers', 'Self-Enrichment Teachers', 'Sewing Machine Operators',
               'Sheet Metal Workers', 'Shipping, Receiving, and Inventory Clerks', 'Shuttle Drivers and Chauffeurs',
               'Skincare Specialists', 'Slaughterers and Meat Packers',
               'Social Scientists and Related Workers, All Other', 'Social Workers, All Other',
               'Social and Community Service Managers', 'Social and Human Service Assistants', 'Software Developers',
               'Software Quality Assurance Analysts and Testers', 'Sound Engineering Technicians',
               'Special Education Teachers, All Other',
               'Special Education Teachers, Kindergarten and Elementary School',
               'Special Education Teachers, Middle School', 'Special Education Teachers, Preschool',
               'Special Effects Artists and Animators', 'Speech-Language Pathologists',
               'Stationary Engineers and Boiler Operators', 'Stockers and Order Fillers',
               'Structural Iron and Steel Workers', 'Structural Metal Fabricators and Fitters',
               'Substance Abuse, Behavioral Disorder, and Mental Health Counselors', 'Surgical Technologists',
               'Surveying and Mapping Technicians', 'Surveyors', 'Switchboard Operators, Including Answering Service',
               'Tailors, Dressmakers, and Custom Sewers', 'Tax Examiners and Collectors, and Revenue Agents',
               'Tax Preparers', 'Teachers and Instructors, All Other', 'Teaching Assistants, Except Postsecondary',
               'Technical Writers', 'Telecommunications Equipment Installers and Repairers, Except Line Installers',
               'Telecommunications Line Installers and Repairers', 'Telemarketers', 'Tellers', 'Therapists, All Other',
               'Tile and Stone Setters', 'Tire Repairers and Changers', 'Title Examiners, Abstractors, and Searchers',
               'Tour and Travel Guides', 'Training and Development Managers', 'Training and Development Specialists',
               'Transportation Inspectors', 'Transportation, Storage, and Distribution Managers', 'Travel Agents',
               'Tutors', 'Umpires, Referees, and Other Sports Officials', 'Upholsterers', 'Urban and Regional Planners',
               'Ushers, Lobby Attendants, and Ticket Takers', 'Veterinarians',
               'Veterinary Assistants and Laboratory Animal Caretakers', 'Veterinary Technologists and Technicians',
               'Waiters and Waitresses', 'Water and Wastewater Treatment Plant and System Operators', 'Web Developers',
               'Web and Digital Interface Designers', 'Weighers, Measurers, Checkers, and Samplers, Recordkeeping',
               'Welders, Cutters, Solderers, and Brazers', 'Writers and Authors']
input_occupation = form_input('Current Occupation(s)', [occupations[0], ], options=occupations, multi=True)
occupation_card = generate_card(
    'Occupation',
    [input_occupation]
)

# Cost of Goods
gas_status = ['regular', 'midgrade', 'premium', 'diesel']
fam_size = ['1 adult', '1 adult 1 child', '1 adult 2 children', '1 adult 3 children', '1 adult 4 children', '2 adults',
            '2 adults 1 child', '2 adults 2 children', '2 adults 3 children', '2 adults 4 children']
input_fuel_type = form_input('Fuel Type', gas_status[0], options=gas_status)
input_fam_size = form_input('Family Size', fam_size[0], options=fam_size, multi=True)

cost_of_goods_card = generate_card(
    'Cost of Goods',
    [input_fuel_type, input_fam_size]
)

# Commute Cost
input_longitude = form_input('Workplace Longitude', '', step=0.00001)
input_latitude = form_input('Workplace Latitude', '', step=0.00001)
input_gas_cost = form_input(label='Fuel Cost', placeholder=3.50, step=0.1)
input_time_cost = form_input(label='Time Cost ($/hr)', placeholder=15)
input_vehicle_mpg = form_input(label='Vehicle MPG', placeholder=25)

commute_card = generate_card(
    'Commute',
    [input_longitude, input_latitude, input_gas_cost, input_time_cost, input_vehicle_mpg]
)

instructions_card = generate_card(
    'Instructions',
    [
        html.H5('1.   Select the city you want to evaluate. Note: only 7 cities are available at this time.'),
        html.H5('2.   Set the input values to match your current or projected situation, then press the "Update" Button.'),
        html.H5(
            '3a.  Summary Tab: Set the "Graphed Value" of the city map to change what value is mapped to the color scale.'),
        html.H5('3b.  Summary Tab: Add Zip Codes of interest to the comparison table.'),
        html.H5('3c.  Summary Tab: Review the "City Average - Comparison Table" to evaluate different cities.'),
        html.H5('4.   Explore other tabs and modify the inputs as needed to dive deeper to the various cost of living inputs.'),

    ]
)

input_card_children = html.Div(
    className='container',
    children=[
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='row mx-auto',
                    children=[
                        instructions_card
                    ]
                ),
                dbc.Form(
                    className='col-md-12 col-lg-6',
                    children=[
                        location_card,
                        tax_card,
                        cost_of_goods_card
                    ]
                ),
                dbc.Form(
                    className='col-md-12 col-lg-6',
                    children=[
                        income_card,
                        housing_card,
                        commute_card,
                    ]
                ),
                html.Div(
                    className='row mx-auto',
                    children=[
                        occupation_card,
                        run_button,
                    ]
                ),
            ]
        ),
    ]
)

input_card = generate_card_card('Input', 'far fa-keyboard', input_card_children, color='info')
