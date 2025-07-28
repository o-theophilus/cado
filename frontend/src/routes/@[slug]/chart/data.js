export let points = [
    {
        id: 'md_ceo',
        x: 'Oluyomi Alararape',
        attributes: { role: 'MD/CEO', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    },
    {
        id: 'executive_assistant',
        parent: 'md_ceo',
        x: '',
        attributes: {
            role: 'Executive Assistant',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'cdo',
        parent: 'md_ceo',
        x: 'Akin Ayodele',
        attributes: { role: 'CDO', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    },
    {
        id: 'coo',
        parent: 'md_ceo',
        x: 'Adewale Taiwo',
        attributes: { role: 'COO', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    },
    {
        id: 'gm_customer_success',
        parent: 'md_ceo',
        x: 'Pamela Chukwuemeka',
        attributes: {
            role: 'GM, Customer Success',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'head_tss',
        parent: 'md_ceo',
        x: 'Josh Adekeye',
        attributes: { role: 'Head, TSS', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    },
    {
        id: 'head_pmo',
        parent: 'md_ceo',
        x: 'Uchenna Uchegbu',
        attributes: { role: 'Head, PMO', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    },
    {
        id: 'cfo',
        parent: 'md_ceo',
        x: 'Lere Adejuwon',
        attributes: { role: 'CFO', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    },
    {
        id: 'head_datazone',
        parent: 'cdo',
        x: 'Olanna Ogbenna',
        attributes: {
            role: 'Head, Datazone',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'solutions_architect_1',
        parent: 'cdo',
        x: 'Oluwaseun Tomisin',
        attributes: {
            role: 'Solutions Architect',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'solutions_architect_2',
        parent: 'cdo',
        x: '',
        attributes: {
            role: 'Solutions Architect',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'presales_consultant_1',
        parent: 'cdo',
        x: 'Adeleke Alarape',
        attributes: {
            role: 'Presales Consultant',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'presales_consultant_2',
        parent: 'cdo',
        x: 'Uwaifo Idenren',
        attributes: {
            role: 'Presales Consultant',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'head_software_engineering',
        parent: 'coo',
        x: 'Adeshina Lawal',
        attributes: {
            role: 'Head, Software Engineering',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'head_sap',
        parent: 'coo',
        x: 'Williams Adebowale',
        attributes: { role: 'Head, SAP', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    },
    {
        id: 'head_hr_and_admin',
        parent: 'coo',
        x: 'Genevieve Okafor',
        attributes: {
            role: 'Head, HR and Admin',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'head_marcomms',
        parent: 'coo',
        x: 'Damilola Adeboye',
        attributes: {
            role: 'Head, Marcomms',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'head_grcs',
        parent: 'coo',
        x: 'Ibukun Amusan',
        attributes: { role: 'Head, GRCS', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    },
    {
        id: 'head_corporate_sales',
        parent: 'gm_customer_success',
        x: 'Michael Onwuka',
        attributes: {
            role: 'Head, Corporate Sales',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'customer_success_consultant_1',
        parent: 'gm_customer_success',
        x: 'Temitope Ajayi',
        attributes: {
            role: 'Customer Success Consultant',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'customer_success_consultant_2',
        parent: 'gm_customer_success',
        x: 'William Bessa-Simons',
        attributes: {
            role: 'Customer Success Consultant',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'managed_services',
        parent: 'head_tss',
        x: '',
        attributes: {
            role: 'Managed Services',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'project_manager_1',
        parent: 'head_pmo',
        x: 'Richie Ogbonnaya',
        attributes: {
            role: 'Project Manager',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'Project_manager_2',
        parent: 'head_pmo',
        x: '',
        attributes: {
            role: 'Project Manager',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 's4hana_consultants',
        parent: 'head_pmo',
        x: '',
        attributes: {
            role: 'S/4HANA Consultants',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'business_analysts',
        parent: 'head_pmo',
        x: 'Daniel Adegeye',
        attributes: {
            role: 'Business Analysts',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'finance_executive',
        parent: 'cfo',
        x: '',
        attributes: {
            role: 'Finance Executive',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'accounts_assistant',
        parent: 'cfo',
        x: 'Abiola Kafidipe',
        attributes: {
            role: 'Accounts Assistant',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'head_product_development',
        parent: 'head_software_engineering',
        x: '',
        attributes: {
            role: 'Head, Product Development',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'head_business_solutions',
        parent: 'head_software_engineering',
        x: '',
        attributes: {
            role: 'Head, Business Solutions',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'hr_executive_1',
        parent: 'head_hr_and_admin',
        x: '',
        attributes: { role: 'HR Executive', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    },
    {
        id: 'hr_admin_executive',
        parent: 'head_hr_and_admin',
        x: '',
        attributes: {
            role: 'HR/Admin Executive',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'admin_manager',
        parent: 'head_hr_and_admin',
        x: 'Evans Samson',
        attributes: {
            role: 'Admin Manager',
            photo: getImgText('images/vector-avatars2/avatar-1.svg')
        }
    },
    {
        id: 'hr_executive_2',
        parent: 'head_hr_and_admin',
        x: 'Kehinde Fagbemi',
        attributes: { role: 'HR Executive', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    },
    {
        id: 'lead_grcs',
        parent: 'head_grcs',
        x: 'Adebola Awelewa',
        attributes: { role: 'Lead, GRCS', photo: getImgText('images/vector-avatars2/avatar-1.svg') }
    }
];
