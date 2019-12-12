context('Actions', () => {
	beforeEach(() => {
		cy.visit('http://localhost:3000/signup')
	})

	//It will go to the signup page to run these tests.
	it('Attempts to signup a user with password < 8 chars', () => {
		cy.get('input[name="username"]').type('test user')
		cy.get('input[name="email"]').type('test@email.com')
		cy.get('input[name="passwordOne"]').type('2short')
		cy.get('input[name="passwordTwo"]').type('2short')
		cy.get('button[type="submit"]').should('not.be.enabled')
		
		//Expect alert with error message	
		// const stub = cy.stub()
		// cy.on('window:alert', stub)
		// cy.get('button[type="submit"]').click()
		// .then(() => {
		// 	expect(stub.getCall(0)).to.be.calledWith('Password length must be >= 8.')
		// })
		
		//Should not redirect
		cy.url().should('not.include', '/home')
	})
    
    //Invalid email fails
	it('Attempts to signup a user with invalid email', () => {
        cy.get('input[name="username"]').type('test user')
        cy.get('input[name="email"]').type('notanemail')
        cy.get('input[name="passwordOne"]').type('irrelevant')
        cy.get('input[name="passwordTwo"]').type('irrelevant')
        cy.get('form').submit()
		cy.get('p').contains('badly formatted')

		//Should not redirect
   		cy.url().should('not.include', '/home')
	 })
})

